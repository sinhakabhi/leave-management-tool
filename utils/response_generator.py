"""
Generate user-friendly responses
"""
from leave_management_ai.config.settings import RESPONSE_TEMPLATES


class ResponseGenerator:
    """Generate formatted responses for users"""
    
    @staticmethod
    def generate_leave_request_response(request_data):
        """Generate response for leave request"""
        if not request_data['is_eligible']:
            return RESPONSE_TEMPLATES['insufficient_balance'].format(**request_data)
        
        return RESPONSE_TEMPLATES['leave_request'].format(**request_data)
    
    @staticmethod
    def generate_confirmation_response(result_data):
        """Generate response for confirmed leave"""
        return RESPONSE_TEMPLATES['leave_confirmed'].format(**result_data)
    
    @staticmethod
    def generate_balance_response(balance_data):
        """Generate response for balance query"""
        return RESPONSE_TEMPLATES['balance_query'].format(**balance_data)
    
    @staticmethod
    def generate_history_response(history_data):
        """Generate response for leave history"""
        if not history_data['history']:
            return "📋 No leave history found.\n\nYou haven't taken any leaves yet."
        
        response = (
            f"📋 Your Leave History:\n"
            f"{'━' * 70}\n\n"
        )
        
        for i, req in enumerate(history_data['history'], 1):
            status_emoji = "✅" if req['status'] == 'approved' else "⏳"
            response += (
                f"{i}. {status_emoji} {req['leave_type']}\n"
                f"   📅 {req['start_date']} → {req['end_date']} ({req['days']} days)\n"
                f"   🕐 Requested on {req['requested_at']}\n\n"
            )
        
        response += f"{'━' * 70}"
        return response.strip()
    
    @staticmethod
    def generate_error_response(error_message):
        """Generate error response"""
        return f"❌ Error: {error_message}"
    
    @staticmethod
    def generate_out_of_scope_response():
        """Generate out of scope response"""
        return (
            "I'm not sure I understood that. I can help you with:\n\n"
            "  • Applying for leave (e.g., 'I need leave from 20th to 25th')\n"
            "  • Checking eligibility (e.g., 'Can I take leave tomorrow?')\n"
            "  • Checking balance (e.g., 'What's my balance?')\n"
            "  • Viewing history (e.g., 'Show my leave history')\n"
            "  • Cancelling future leaves (e.g., 'Cancel my leave on 20th')\n\n"
            "What would you like to do?"
        )
    
    @staticmethod
    def generate_cancellation_response():
        """Generate cancellation response"""
        return "Your pending leave request has been cancelled."
    
    @staticmethod
    def generate_no_pending_response():
        """Generate response when no pending request exists"""
        return "There is no pending leave request to confirm. Please create a new leave request first."
    
    @staticmethod
    def generate_eligibility_yes_response(eligibility_data):
        """Generate positive eligibility response"""
        return RESPONSE_TEMPLATES['eligibility_yes'].format(**eligibility_data)
    
    @staticmethod
    def generate_eligibility_no_weekend_response(eligibility_data):
        """Generate weekend eligibility response"""
        return RESPONSE_TEMPLATES['eligibility_no_weekend'].format(**eligibility_data)
    
    @staticmethod
    def generate_eligibility_no_balance_response(eligibility_data):
        """Generate insufficient balance eligibility response"""
        return RESPONSE_TEMPLATES['eligibility_no_balance'].format(**eligibility_data)
    
    @staticmethod
    def generate_overlapping_leaves_response(overlap_data):
        """Generate response for overlapping leaves"""
        overlap_details = []
        for i, leave in enumerate(overlap_data['overlapping_leaves'], 1):
            overlap_details.append(
                f"{i}. {leave['leave_type']}\n"
                f"   📅 {leave['start_date']} → {leave['end_date']} ({leave['days']} days)"
            )
        
        return RESPONSE_TEMPLATES['overlapping_leaves'].format(
            overlap_details='\n'.join(overlap_details),
            start_date=overlap_data['overlapping_leaves'][0]['start_date'],
            end_date=overlap_data['overlapping_leaves'][-1]['end_date']
        )
    
    @staticmethod
    def generate_leaves_cancelled_response(cancel_data):
        """Generate response for cancelled leaves"""
        cancelled_details = []
        for i, leave in enumerate(cancel_data['cancelled_leaves'], 1):
            cancelled_details.append(
                f"{i}. {leave['leave_type']}\n"
                f"   📅 {leave['start_date']} → {leave['end_date']}\n"
                f"   ↩️  Restored: {leave['days']} days → Balance: {leave['restored_balance']} days"
            )
        
        return RESPONSE_TEMPLATES['leaves_cancelled'].format(
            cancelled_details='\n'.join(cancelled_details),
            total_restored=cancel_data['total_restored']
        )
    
    @staticmethod
    def generate_cancel_past_leave_error():
        """Generate error for trying to cancel past leave"""
        return RESPONSE_TEMPLATES['cancel_past_leave_error']
    
    @staticmethod
    def generate_no_leaves_to_cancel():
        """Generate response when no leaves found to cancel"""
        return RESPONSE_TEMPLATES['no_leaves_to_cancel']