"""
Main application - Leave Management AI
"""
from leave_management_ai.nlp.entity_character import EntityExtractor
from leave_management_ai.nlp.intent_classifier import IntentClassifier
from services.leave_service import LeaveService
from utils.response_generator import ResponseGenerator


class LeaveManagementAI:
    """Main AI assistant for leave management"""
    
    def __init__(self):
        print("🚀 Initializing Leave Management AI...")
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()
        self.leave_service = LeaveService()
        self.response_generator = ResponseGenerator()
        self.current_employee_id = None
        print("✓ System ready!\n")
    
    def set_employee_id(self, employee_id):
        """Set the current logged-in employee"""
        # Validate employee exists
        is_valid, result = self.leave_service.validate_employee(employee_id)
        if is_valid:
            self.current_employee_id = employee_id
            employee_name = result[1]  # Name is second column
            return True, f"Welcome, {employee_name}! (ID: {employee_id})"
        else:
            return False, result
    
    def process_query(self, user_input):
        """
        Process user query and return response
        
        Args:
            user_input: User's text input
        
        Returns:
            Response string
        """
        # Step 1: Classify intent
        intent = self.intent_classifier.classify(user_input)
        
        # Step 2: Extract entities
        entities = self.entity_extractor.extract_all_entities(user_input)
        
        # Use current session employee ID if not found in text
        if not entities['employee_id'] and self.current_employee_id:
            entities['employee_id'] = self.current_employee_id
        
        # Step 3: Route to appropriate handler
        try:
            if intent == 'apply_leave':
                return self._handle_leave_application(entities)
            
            elif intent == 'confirm_leave':
                return self._handle_leave_confirmation(entities)
            
            elif intent == 'cancel_request':
                return self._handle_cancellation(entities)
            
            elif intent == 'check_balance':
                return self._handle_balance_check(entities)
            
            elif intent == 'leave_history':
                return self._handle_leave_history(entities)
            
            else:
                return self.response_generator.generate_out_of_scope_response()
        
        except Exception as e:
            return self.response_generator.generate_error_response(str(e))
    
    def _handle_leave_application(self, entities):
        """Handle leave application request"""
        employee_id = entities['employee_id']
        
        # Validate employee
        is_valid, result = self.leave_service.validate_employee(employee_id)
        if not is_valid:
            return self.response_generator.generate_error_response(result)
        
        # Validate dates
        if not entities['start_date'] or not entities['end_date']:
            return self.response_generator.generate_error_response(
                "Could not understand the dates. Please specify dates clearly.\n"
                "Examples: 'leave from tomorrow to Friday' or 'leave on 20th Jan'"
            )
        
        # Create leave request
        request_data = self.leave_service.create_leave_request(
            employee_id,
            entities['leave_type'],
            entities['start_date'],
            entities['end_date'],
            entities['days_count']
        )
        
        return self.response_generator.generate_leave_request_response(request_data)
    
    def _handle_leave_confirmation(self, entities):
        """Handle leave confirmation"""
        employee_id = entities['employee_id']
        
        # Validate employee
        is_valid, result = self.leave_service.validate_employee(employee_id)
        if not is_valid:
            return self.response_generator.generate_error_response(result)
        
        # Confirm leave
        success, result_data = self.leave_service.confirm_leave_request(employee_id)
        
        if success:
            return self.response_generator.generate_confirmation_response(result_data)
        else:
            if 'error' in result_data:
                if 'No pending' in result_data['error']:
                    return self.response_generator.generate_no_pending_response()
                else:
                    error_msg = result_data['error']
                    if 'shortage' in result_data:
                        error_msg += f"\nYou have {result_data['current_balance']} days but need {result_data['requested']} days."
                    return self.response_generator.generate_error_response(error_msg)
            return self.response_generator.generate_error_response("Failed to confirm leave")
    
    def _handle_cancellation(self, entities):
        """Handle leave cancellation"""
        employee_id = entities['employee_id']
        
        if not employee_id:
            return self.response_generator.generate_error_response(
                "Could not identify employee ID"
            )
        
        # Validate employee
        is_valid, result = self.leave_service.validate_employee(employee_id)
        if not is_valid:
            return self.response_generator.generate_error_response(result)
        
        self.leave_service.cancel_pending_request(employee_id)
        return self.response_generator.generate_cancellation_response()
    
    def _handle_balance_check(self, entities):
        """Handle balance check request"""
        employee_id = entities['employee_id']
        
        # Validate employee
        is_valid, result = self.leave_service.validate_employee(employee_id)
        if not is_valid:
            return self.response_generator.generate_error_response(result)
        
        # Get balance
        balance_data = self.leave_service.get_leave_balance(employee_id)
        return self.response_generator.generate_balance_response(balance_data)
    
    def _handle_leave_history(self, entities):
        """Handle leave history request"""
        employee_id = entities['employee_id']
        
        # Validate employee
        is_valid, result = self.leave_service.validate_employee(employee_id)
        if not is_valid:
            return self.response_generator.generate_error_response(result)
        
        # Get history
        history_data = self.leave_service.get_leave_history(employee_id)
        return self.response_generator.generate_history_response(history_data)


def main():
    """Main function to run the AI assistant"""
    print("=" * 70)
    print("              LEAVE MANAGEMENT AI ASSISTANT")
    print("=" * 70)
    print()
    
    # Initialize AI
    ai = LeaveManagementAI()
    
    # Employee login
    print("Please enter your Employee ID to continue")
    print("Available IDs: EMP123, EMP124, EMP125, E001, E002")
    print("-" * 70)
    
    while True:
        try:
            employee_id = input("\nEmployee ID: ").strip().upper()
            
            if not employee_id:
                continue
            
            if employee_id in ['QUIT', 'EXIT']:
                print("\nGoodbye! 👋")
                return
            
            success, message = ai.set_employee_id(employee_id)
            
            if success:
                print(f"\n✓ {message}")
                print("\n" + "=" * 70)
                print("What can I help you with today?")
                print("-" * 70)
                print("Examples:")
                print("  • I need leave from tomorrow to Friday")
                print("  • What's my leave balance?")
                print("  • Show my leave history")
                print("  • Type 'logout' to switch employee or 'quit' to exit")
                print("=" * 70)
                break
            else:
                print(f"\n✗ {message}")
                print("Please try again or type 'quit' to exit.")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            return
    
    # Main interaction loop
    print()
    while True:
        try:
            user_input = input(f"{ai.current_employee_id}: ").strip()
            
            if not user_input:
                continue
            
            # Handle logout
            if user_input.lower() in ['logout', 'switch', 'change employee']:
                print(f"\n{'=' * 70}")
                print("Logging out...")
                ai.current_employee_id = None
                main()  # Restart login
                return
            
            # Handle quit
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nThank you for using Leave Management AI. Goodbye! 👋")
                break
            
            # Process query
            response = ai.process_query(user_input)
            print(f"\nAssistant: {response}\n")
            print("-" * 70)
        
        except KeyboardInterrupt:
            print("\n\nLogging out... Goodbye! 👋")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}\n")


if __name__ == "__main__":
    main()