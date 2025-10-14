"""
Unit tests for the Trama Caribe Slack bot.

Tests the core functionality of greeting detection and inactivity tracking.
"""

import unittest
import time
from bot import has_greeting, should_respond, INACTIVITY_SECONDS


class TestGreetingDetection(unittest.TestCase):
    """Test cases for greeting detection."""
    
    def test_has_greeting_with_hola(self):
        """Test that 'hola' is recognized as a greeting."""
        self.assertTrue(has_greeting("hola, com estàs?"))
        self.assertTrue(has_greeting("Hola everyone"))
        self.assertTrue(has_greeting("HOLA!!!"))
        self.assertTrue(has_greeting("  hola  "))
    
    def test_has_greeting_with_bon_dia(self):
        """Test that 'bon dia' is recognized as a greeting."""
        self.assertTrue(has_greeting("bon dia team"))
        self.assertTrue(has_greeting("Bon dia! Com va?"))
    
    def test_has_greeting_with_ei(self):
        """Test that 'ei' is recognized as a greeting."""
        self.assertTrue(has_greeting("ei, necessito ajuda"))
        self.assertTrue(has_greeting("Ei! Què tal?"))
    
    def test_has_greeting_with_hey(self):
        """Test that 'hey' is recognized as a greeting."""
        self.assertTrue(has_greeting("hey everyone"))
        self.assertTrue(has_greeting("Hey, can you help?"))
    
    def test_has_greeting_with_hello(self):
        """Test that 'hello' is recognized as a greeting."""
        self.assertTrue(has_greeting("hello team"))
        self.assertTrue(has_greeting("Hello! How are you?"))
    
    def test_no_greeting(self):
        """Test that messages without greetings are detected."""
        self.assertFalse(has_greeting("Can someone review my PR?"))
        self.assertFalse(has_greeting("I need help with this bug"))
        self.assertFalse(has_greeting("Quick question about the project"))
    
    def test_greeting_not_at_start(self):
        """Test that greetings not at the start are not recognized."""
        self.assertFalse(has_greeting("I said hola yesterday"))
        self.assertFalse(has_greeting("Can you say hello to them?"))
    
    def test_empty_message(self):
        """Test that empty messages don't have greetings."""
        self.assertFalse(has_greeting(""))
        self.assertFalse(has_greeting(None))
    
    def test_partial_match(self):
        """Test that partial matches don't count as greetings."""
        # "hola" should not match "holaa" without word boundary
        self.assertTrue(has_greeting("hola team"))  # Should match
        self.assertFalse(has_greeting("wholesome message"))  # Should not match "hola"


class TestInactivityTracking(unittest.TestCase):
    """Test cases for inactivity tracking."""
    
    def test_should_not_respond_first_message(self):
        """Test that bot doesn't respond to first message from user."""
        user_id = "U123"
        channel_id = "C123"
        current_time = time.time()
        
        # First message - should not respond
        self.assertFalse(should_respond(user_id, channel_id, current_time))
    
    def test_should_respond_after_inactivity(self):
        """Test that bot responds after period of inactivity."""
        from bot import user_last_message
        
        user_id = "U456"
        channel_id = "C456"
        key = (user_id, channel_id)
        
        # Simulate a message from 5 hours ago
        old_time = time.time() - (5 * 3600)
        user_last_message[key] = old_time
        
        current_time = time.time()
        
        # Should respond due to inactivity
        self.assertTrue(should_respond(user_id, channel_id, current_time))
    
    def test_should_not_respond_within_threshold(self):
        """Test that bot doesn't respond within inactivity threshold."""
        from bot import user_last_message
        
        user_id = "U789"
        channel_id = "C789"
        key = (user_id, channel_id)
        
        # Simulate a message from 2 hours ago (less than threshold)
        recent_time = time.time() - (2 * 3600)
        user_last_message[key] = recent_time
        
        current_time = time.time()
        
        # Should not respond - within threshold
        self.assertFalse(should_respond(user_id, channel_id, current_time))
    
    def test_should_respond_exactly_at_threshold(self):
        """Test behavior at exact inactivity threshold."""
        from bot import user_last_message
        
        user_id = "U101"
        channel_id = "C101"
        key = (user_id, channel_id)
        
        # Simulate a message exactly at threshold
        threshold_time = time.time() - INACTIVITY_SECONDS
        user_last_message[key] = threshold_time
        
        current_time = time.time()
        
        # Should respond at or after threshold
        self.assertTrue(should_respond(user_id, channel_id, current_time))
    
    def test_different_channels_tracked_separately(self):
        """Test that activity is tracked per channel."""
        from bot import user_last_message
        
        user_id = "U202"
        channel1 = "C201"
        channel2 = "C202"
        
        # User was active 5 hours ago in channel1
        old_time = time.time() - (5 * 3600)
        user_last_message[(user_id, channel1)] = old_time
        
        current_time = time.time()
        
        # Should respond in channel1 (inactive)
        self.assertTrue(should_respond(user_id, channel1, current_time))
        
        # Should not respond in channel2 (first message there)
        self.assertFalse(should_respond(user_id, channel2, current_time))


if __name__ == "__main__":
    unittest.main()
