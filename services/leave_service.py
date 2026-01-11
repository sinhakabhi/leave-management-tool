"""
Leave management business logic
"""
from datetime import datetime, timedelta
from leave_management_ai.database.operations import (
    EmployeeOperations,
    LeaveBalanceOperations,
    LeaveRequestOperations,
    LeaveTransactionOperations,
    PendingConfirmationOperations
)
from leave_management_ai.config.settings import LEAVE_TYPES, BUSINESS_RULES


class LeaveService:
    """Business logic for leave management"""
    
    def __init__(self):
        self.employee_ops = EmployeeOperations()
        self.balance_ops = LeaveBalanceOperations()
        self.request_ops = LeaveRequestOperations()
        self.transaction_ops = LeaveTransactionOperations()
        self.pending_ops = PendingConfirmationOperations()
    
    def validate_employee(self, employee_id):
        """
        Validate if employee exists
        Returns (is_valid, employee_data/error_message)
        """
        if not employee_id:
            return False, "Employee ID is required"
        
        if not self.employee_ops.employee_exists(employee_id):
            return False, f"Employee {employee_id} not found in the system"
        
        employee = self.employee_ops.get_employee(employee_id)
        return True, employee
    
    def check_leave_eligibility(self, employee_id, leave_type, days_requested):
        """
        Check if employee has enough leave balance
        Returns (is_eligible, current_balance, remaining_balance/shortage)
        """
        current_balance = self.balance_ops.get_balance(employee_id, leave_type)
        remaining_balance = current_balance - days_requested
        
        # Check minimum balance rule
        min_balance = BUSINESS_RULES['min_leave_balance']
        is_eligible = remaining_balance >= min_balance
        
        return is_eligible, current_balance, remaining_balance
    
    def create_leave_request(self, employee_id, leave_type, start_date, end_date, days_count):
        """
        Create a pending leave request
        Returns dict with request details
        """
        # Check for overlapping leaves first
        overlapping = self.request_ops.check_overlapping_leaves(employee_id, start_date, end_date)
        
        if overlapping:
            # Format overlapping leave details
            overlap_details = []
            for leave in overlapping:
                leave_id, ltype, lstart, lend, ldays = leave
                overlap_details.append({
                    'id': leave_id,
                    'leave_type': LEAVE_TYPES.get(ltype, ltype),
                    'start_date': lstart.strftime('%Y-%m-%d'),
                    'end_date': lend.strftime('%Y-%m-%d'),
                    'days': float(ldays)
                })
            
            return {
                'employee_id': employee_id,
                'has_overlap': True,
                'overlapping_leaves': overlap_details,
                'error': 'You already have approved leave(s) for these dates'
            }
        
        # Check eligibility
        is_eligible, current_balance, remaining_balance = self.check_leave_eligibility(
            employee_id, leave_type, days_count
        )
        
        # Create pending confirmation
        self.pending_ops.create_pending(
            employee_id, leave_type, start_date, end_date, days_count
        )
        
        return {
            'employee_id': employee_id,
            'leave_type': LEAVE_TYPES.get(leave_type, leave_type),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'days': days_count,
            'current_balance': current_balance,
            'remaining_balance': remaining_balance,
            'is_eligible': is_eligible,
            'has_overlap': False,
            'shortage': days_count - current_balance if not is_eligible else 0
        }
    
    def confirm_leave_request(self, employee_id):
        """
        Confirm and apply pending leave request
        Returns (success, result_dict)
        """
        # Get pending confirmation
        pending = self.pending_ops.get_pending(employee_id)
        
        if not pending:
            return False, {
                'error': 'No pending leave request found. Please create a new leave request first.'
            }
        
        leave_type, start_date, end_date, days_count = pending
        
        # Check eligibility again (balance might have changed)
        is_eligible, current_balance, remaining_balance = self.check_leave_eligibility(
            employee_id, leave_type, days_count
        )
        
        if not is_eligible:
            self.pending_ops.clear_pending(employee_id)
            return False, {
                'error': 'Insufficient leave balance',
                'current_balance': current_balance,
                'requested': days_count,
                'shortage': days_count - current_balance
            }
        
        # Apply leave
        # 1. Create leave request record
        request_id = self.request_ops.create_request(
            employee_id, leave_type, start_date, end_date, days_count
        )
        
        # 2. Deduct from balance
        new_balance = self.balance_ops.deduct_balance(employee_id, leave_type, days_count)
        
        # 3. Log transaction
        self.transaction_ops.log_transaction(
            employee_id, leave_type, 'debit', days_count,
            current_balance, new_balance,
            f"Leave from {start_date} to {end_date}"
        )
        
        # 4. Clear pending confirmation
        self.pending_ops.clear_pending(employee_id)
        
        return True, {
            'request_id': request_id,
            'employee_id': employee_id,
            'leave_type': LEAVE_TYPES.get(leave_type, leave_type),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'days': days_count,
            'remaining_balance': new_balance
        }
    
    def get_leave_balance(self, employee_id):
        """
        Get all leave balances for employee
        Returns dict with balance details
        """
        balances = self.balance_ops.get_all_balances(employee_id)
        
        balance_details = []
        for leave_type, balance in balances.items():
            # Add visual indicator for balance level
            if balance >= 10:
                indicator = "🟢"
            elif balance >= 5:
                indicator = "🟡"
            else:
                indicator = "🔴"
            
            balance_details.append(
                f"{indicator} {LEAVE_TYPES.get(leave_type, leave_type)}: {balance} days"
            )
        
        return {
            'employee_id': employee_id,
            'balances': balances,
            'balance_details': '\n'.join(balance_details) if balance_details else 'No leave balance found'
        }
    
    def get_leave_history(self, employee_id, limit=10):
        """
        Get recent leave history for employee
        Returns list of leave requests
        """
        requests = self.request_ops.get_employee_requests(employee_id, limit)
        
        history = []
        for req in requests:
            req_id, leave_type, start_date, end_date, days, status, requested_at = req
            history.append({
                'id': req_id,
                'leave_type': LEAVE_TYPES.get(leave_type, leave_type),
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days': float(days),
                'status': status,
                'requested_at': requested_at.strftime('%Y-%m-%d %H:%M')
            })
        
        return {
            'employee_id': employee_id,
            'history': history
        }
    
    def cancel_pending_request(self, employee_id):
        """Cancel any pending leave request"""
        self.pending_ops.clear_pending(employee_id)
        return {
            'employee_id': employee_id,
            'message': 'Pending leave request cancelled'
        }
    
    def cancel_approved_leaves(self, employee_id, start_date, end_date):
        """
        Cancel approved leaves in a date range
        Returns (success, result_dict)
        """
        from datetime import datetime
        
        today = datetime.now().date()
        
        # Check if dates are in the future
        if start_date <= today:
            return False, {
                'error': 'past_leave',
                'message': 'You can only cancel future leaves. Past or current leaves cannot be cancelled.'
            }
        
        # Get approved leaves in the range
        leaves = self.request_ops.get_leaves_in_range(employee_id, start_date, end_date)
        
        if not leaves:
            return False, {
                'error': 'no_leaves',
                'message': f'No approved leaves found between {start_date.strftime("%Y-%m-%d")} and {end_date.strftime("%Y-%m-%d")}'
            }
        
        # Cancel each leave and restore balance
        cancelled_leaves = []
        total_restored = 0
        
        for leave in leaves:
            leave_id, leave_type, lstart, lend, days = leave
            
            # Cancel the leave request
            result = self.request_ops.cancel_leave_request(leave_id)
            
            if result:
                # Restore balance
                current_balance = self.balance_ops.get_balance(employee_id, leave_type)
                new_balance = current_balance + float(days)
                self.balance_ops.update_balance(employee_id, leave_type, new_balance)
                
                # Log transaction
                self.transaction_ops.log_transaction(
                    employee_id, leave_type, 'credit', float(days),
                    current_balance, new_balance,
                    f"Cancelled leave from {lstart} to {lend}"
                )
                
                cancelled_leaves.append({
                    'id': leave_id,
                    'leave_type': LEAVE_TYPES.get(leave_type, leave_type),
                    'start_date': lstart.strftime('%Y-%m-%d'),
                    'end_date': lend.strftime('%Y-%m-%d'),
                    'days': float(days),
                    'restored_balance': new_balance
                })
                
                total_restored += float(days)
        
        return True, {
            'employee_id': employee_id,
            'cancelled_leaves': cancelled_leaves,
            'total_restored': total_restored
        }
    
    def check_leave_eligibility_for_date(self, employee_id, leave_type, target_date, days_requested=1):
        """
        Check if employee is eligible for leave on a specific date
        Returns (eligible, reason_data)
        """
        from datetime import datetime
        
        # Check if it's a weekend
        is_weekend = target_date.weekday() >= 5  # Saturday=5, Sunday=6
        
        # Get current balance
        current_balance = self.balance_ops.get_balance(employee_id, leave_type)
        
        # Prepare response data
        date_str = target_date.strftime('%Y-%m-%d')
        day_name = target_date.strftime('%A')
        
        # Determine date phrase for response
        today = datetime.now().date()
        if target_date == today:
            date_phrase = "today"
        elif target_date == today + timedelta(days=1):
            date_phrase = "tomorrow"
        else:
            date_phrase = f"on {target_date.strftime('%B %d')}"
        
        # Case 1: Weekend (not eligible)
        if is_weekend and not BUSINESS_RULES['weekend_counts']:
            return False, {
                'type': 'weekend',
                'date': date_str,
                'day_name': day_name
            }
        
        # Case 2: Insufficient balance
        if current_balance < days_requested:
            return False, {
                'type': 'no_balance',
                'date': date_str,
                'day_name': day_name,
                'balance': current_balance,
                'required': days_requested
            }
        
        # Case 3: Eligible!
        return True, {
            'type': 'eligible',
            'date': date_str,
            'day_name': day_name,
            'balance': current_balance,
            'after_balance': current_balance - days_requested,
            'date_phrase': date_phrase
        }