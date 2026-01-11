"""
Intent classification for user queries
"""
import re


class IntentClassifier:
    """Classify user intent from text"""
    
    def __init__(self):
        # Intent patterns with keywords
        self.intent_patterns = {
            'apply_leave': [
                r'\b(need|want|apply|request|take|book)\s+(leave|time off|vacation)',
                r'\b(need|want|apply|request|take|book)\s+(sick|casual|vacation|general)?\s*leave',
                r'\b(i|I)\s+(will|would|shall)\s+be\s+(on\s+)?leave',
                r'\b(going|planning)\s+on\s+leave',
                r'\bleave\s+(from|on|for)',
                r'\bwill\s+not\s+be\s+(available|present|coming|in office)',
                r'\boff\s+(on|from|for)',
                r'\bwill\s+be\s+(absent|away|out)',
                r'\b(apply|request|need|want|take).*(leave|off)',
                r'\bleave\s+on\s+\w+\s+and\s+\w+',  # "leave on Monday and Tuesday"
                r'\bon\s+\w+\s+and\s+\w+',  # "on Monday and Tuesday"
                r'\b(sick|casual|vacation|medical)\s+leave',  # "sick leave", "casual leave"
            ],
            'check_eligibility': [
                r'^(can|could|may)\s+(i|I)\s+(take|get|have|apply)',
                r'^(am i|is it)\s+(allowed|able|possible|ok|okay|eligible)',
                r'\b(can|could|may)\s+(i|I)\s+.*\s*(leave|off)',
                r'\beligible\s+for\s+leave',
                r'\ballowed\s+to\s+(take\s+)?leave',
                r'\bpossible\s+to\s+(take\s+)?leave',
                r'\b(can|could)\s+(i|I)\s+',  # General "can I" questions
            ],
            'cancel_approved_leave': [
                r'^cancel\s+',  # Starts with "cancel"
                r'^remove\s+',  # Starts with "remove"
                r'^delete\s+',  # Starts with "delete"
                r'^withdraw\s+', # Starts with "withdraw"
                r'\bcancel\s+(my\s+)?(sick|casual|vacation|general)?\s*(leave|leaves)',
                r'\bcancel\s+.*\s+(leave|leaves)',
                r'\bremove\s+(my\s+)?leave',
                r'\bdelete\s+(my\s+)?leave',
                r'\bwithdraw\s+(my\s+)?leave',
                r'\brevert\s+(my\s+)?leave',
            ],
            'confirm_leave': [
                r'\b(yes|yep|yeah|sure|ok|okay|confirm|approved?|accept|proceed)',
                r'\b(go ahead|do it|please proceed)',
            ],
            'cancel_request': [
                r'\b(no|nope|nah|cancel|reject|deny|decline|nevermind)',
                r'\b(don\'t|do not)\s+(want|need)',
            ],
            'check_balance': [
                r'\b(how many|how much|what\'s|what is|check|show|tell)\s+.*(leave|balance)',
                r'\bleave\s+(balance|remaining|left|available)',
                r'\bmy\s+balance',
                r'\bremaining\s+(leave|days)',
            ],
            'leave_history': [
                r'\b(show|view|check|get|display)\s+.*(history|past|previous|record)',
                r'\bleave\s+history',
                r'\bpast\s+leaves',
                r'\bmy\s+(leave\s+)?requests',
            ],
        }
    
    def classify(self, text):
        """
        Classify user intent from text
        Returns intent string or 'unknown'
        """
        text_lower = text.lower()
        
        # PRIORITY 1: Cancel approved leave (check FIRST to prevent misclassification)
        # This must come before apply_leave since "cancel sick leave" contains "sick leave"
        for pattern in self.intent_patterns.get('cancel_approved_leave', []):
            if re.search(pattern, text_lower):
                return 'cancel_approved_leave'
        
        # PRIORITY 2: Check eligibility intent (questions with modal verbs)
        for pattern in self.intent_patterns.get('check_eligibility', []):
            if re.search(pattern, text_lower):
                return 'check_eligibility'
        
        # PRIORITY 3: Simple confirmations
        confirmation_words = ['yes', 'yep', 'yeah', 'ok', 'okay', 'confirm', 'sure']
        if text_lower.strip() in confirmation_words:
            return 'confirm_leave'
        
        # PRIORITY 4: Simple cancellations (for pending requests)
        cancel_words = ['no', 'nope', 'nah']
        if text_lower.strip() in cancel_words:
            return 'cancel_request'
        
        # PRIORITY 5: Check other intents
        for intent, patterns in self.intent_patterns.items():
            if intent in ['check_eligibility', 'cancel_approved_leave']:  # Already checked above
                continue
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent
        
        return 'unknown'
    
    def get_confidence(self, text, intent):
        """
        Get confidence score for an intent (simple heuristic)
        Returns float between 0 and 1
        """
        if intent == 'unknown':
            return 0.0
        
        text_lower = text.lower()
        patterns = self.intent_patterns.get(intent, [])
        
        # Count matching patterns
        matches = 0
        for pattern in patterns:
            if re.search(pattern, text_lower):
                matches += 1
        
        # Simple confidence: more matches = higher confidence
        if matches > 0:
            return min(0.6 + (matches * 0.2), 1.0)
        
        return 0.0