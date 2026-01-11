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
                r'\b(i|I)\s+(will|would|shall)\s+be\s+(on\s+)?leave',
                r'\b(going|planning)\s+on\s+leave',
                r'\bleave\s+(from|on|for)',
                r'\bwill\s+not\s+be\s+(available|present|coming|in office)',
                r'\boff\s+(on|from|for)',
                r'\bwill\s+be\s+(absent|away|out)',
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
        
        # Check each intent pattern
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent
        
        # Check for simple confirmation words (for confirmation flow)
        confirmation_words = ['yes', 'yep', 'yeah', 'ok', 'okay', 'confirm', 'sure']
        if text_lower.strip() in confirmation_words:
            return 'confirm_leave'
        
        # Check for simple cancellation words
        cancel_words = ['no', 'nope', 'cancel', 'nah']
        if text_lower.strip() in cancel_words:
            return 'cancel_request'
        
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