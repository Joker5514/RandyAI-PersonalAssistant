#!/usr/bin/env python3
"""
RandyAI Personal Assistant Test Suite
Comprehensive testing for all components
"""

import unittest
import asyncio
import tempfile
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.randy_ai import RandyAI, UserPreferences
from integrations.multi_platform import MultiPlatformIntegrator, EnhancedRandyAI
from autonomous.scheduler import AutonomousScheduler, QuestionGenerator

class TestRandyAICore(unittest.TestCase):
    """Test core RandyAI functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Use temporary database for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, "test_randy_ai.db")
        
        # Create RandyAI instance with test database
        self.randy_ai = RandyAI()
        self.randy_ai.db_path = Path(self.test_db_path)
        self.randy_ai.init_database()
        
    def tearDown(self):
        """Clean up test environment"""
        # Remove test database
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        os.rmdir(self.temp_dir)
        
    def test_user_preferences_initialization(self):
        """Test user preferences are correctly initialized"""
        prefs = self.randy_ai.preferences
        
        self.assertEqual(prefs.name, "Randy Jordan")
        self.assertEqual(prefs.location, "Mobile, Alabama")
        self.assertEqual(prefs.zip_code, "36605")
        self.assertEqual(prefs.vehicle, "2020 Toyota Corolla LE")
        self.assertIn("Uber", prefs.work)
        self.assertIn("AI Development", prefs.interests)
        
    def test_memory_operations(self):
        """Test memory save and retrieval"""
        # Save test data
        test_key = "test_memory_key"
        test_value = "test_memory_value"
        
        self.randy_ai.save_memory(test_key, test_value, "test")
        
        # Verify it's in memory
        self.assertIn(test_key, self.randy_ai.memory)
        self.assertEqual(self.randy_ai.memory[test_key], test_value)
        
        # Test complex data
        complex_data = {"list": [1, 2, 3], "dict": {"nested": True}}
        self.randy_ai.save_memory("complex", complex_data, "test")
        self.assertEqual(self.randy_ai.memory["complex"], complex_data)
        
    def test_learning_system(self):
        """Test learning from interactions"""
        input_data = "Test input for learning"
        output_data = "Test output response"
        success_score = 0.85
        
        initial_count = len(self.randy_ai.learning_data)
        
        self.randy_ai.learn_from_interaction(input_data, output_data, success_score)
        
        # Verify learning data was added
        self.assertEqual(len(self.randy_ai.learning_data), initial_count + 1)
        
        latest_learning = self.randy_ai.learning_data[-1]
        self.assertEqual(latest_learning['input'], input_data)
        self.assertEqual(latest_learning['output'], output_data)
        self.assertEqual(latest_learning['success'], success_score)
        
    def test_task_management(self):
        """Test task creation and retrieval"""
        task_title = "Test Task"
        task_description = "Test task description"
        priority = 7
        due_date = datetime.now() + timedelta(hours=2)
        
        # Create task
        task_id = self.randy_ai.create_task(task_title, task_description, priority, due_date)
        self.assertIsInstance(task_id, int)
        
        # Retrieve tasks
        pending_tasks = self.randy_ai.get_pending_tasks()
        self.assertGreater(len(pending_tasks), 0)
        
        # Check task details
        created_task = next((t for t in pending_tasks if t['id'] == task_id), None)
        self.assertIsNotNone(created_task)
        self.assertEqual(created_task['title'], task_title)
        self.assertEqual(created_task['priority'], priority)
        
    def test_daily_update_generation(self):
        """Test daily update report generation"""
        # Add some test data
        self.randy_ai.create_task("Test Task 1", "Description 1", 8)
        self.randy_ai.create_task("Test Task 2", "Description 2", 6)
        self.randy_ai.learn_from_interaction("input1", "output1", 0.9)
        self.randy_ai.save_memory("test_key1", "test_value1", "test")
        
        # Generate update
        update = self.randy_ai.daily_update()
        
        self.assertIsInstance(update, str)
        self.assertIn("Daily Update", update)
        self.assertIn("Pending Tasks:", update)
        self.assertIn("Memory Items:", update)
        
    def test_status_reporting(self):
        """Test system status reporting"""
        status = self.randy_ai.get_status()
        
        self.assertIsInstance(status, dict)
        self.assertIn('memory_items', status)
        self.assertIn('learning_items', status)
        self.assertIn('pending_tasks', status)
        self.assertIn('last_update', status)
        self.assertIn('preferences', status)
        
class TestMultiPlatformIntegrator(unittest.TestCase):
    """Test multi-platform integration functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, "test_integrator.db")
        
        self.randy_ai = RandyAI()
        self.randy_ai.db_path = Path(self.test_db_path)
        self.randy_ai.init_database()
        
        self.integrator = MultiPlatformIntegrator(self.randy_ai)
        
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        os.rmdir(self.temp_dir)
        
    def test_api_configuration(self):
        """Test API configuration"""
        test_key = "test_api_key_12345"
        
        # Configure API
        result = self.integrator.configure_api('perplexity', test_key)
        self.assertTrue(result)
        
        # Verify configuration
        self.assertEqual(self.integrator.apis['perplexity'].key, test_key)
        
        # Test invalid service
        result = self.integrator.configure_api('invalid_service', test_key)
        self.assertFalse(result)
        
    def test_handoff_creation(self):
        """Test project handoff functionality"""
        project_data = {
            "name": "TestProject",
            "description": "Test project for handoff",
            "code": "print('Hello, World!')",
            "requirements": ["python>=3.8"]
        }
        instructions = "Continue development with these specifications"
        
        # Create handoff (this will run synchronously for testing)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                self.integrator.handoff_to_deepagent(project_data, instructions)
            )
            
            self.assertIsInstance(result, dict)
            self.assertTrue(result.get('success', False))
            self.assertIn('handoff_file', result)
            
            # Verify file was created
            filename = result['handoff_file']
            self.assertTrue(os.path.exists(filename))
            
            # Clean up
            os.remove(filename)
            
        finally:
            loop.close()
            
    def test_space_config_creation(self):
        """Test AI space configuration creation"""
        space_name = "TestSpace"
        personality = "helpful_assistant"
        purpose = "Testing AI space creation"
        
        config = self.integrator.create_space_config(space_name, personality, purpose)
        
        self.assertIsInstance(config, dict)
        self.assertEqual(config['name'], space_name)
        self.assertEqual(config['personality'], personality)
        self.assertEqual(config['purpose'], purpose)
        self.assertEqual(config['owner'], "Randy Jordan")
        self.assertTrue(config['memory_access'])
        self.assertTrue(config['learning_enabled'])
        
    def test_integration_status(self):
        """Test integration status reporting"""
        status = self.integrator.get_integration_status()
        
        self.assertIsInstance(status, dict)
        self.assertIn('perplexity', status)
        self.assertIn('abacus', status)
        self.assertIn('deepagent', status)
        
        for platform, info in status.items():
            self.assertIn('configured', info)
            self.assertIn('active', info)
            self.assertIn('endpoint', info)
            
class TestAutonomousScheduler(unittest.TestCase):
    """Test autonomous scheduler functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, "test_scheduler.db")
        
        self.randy_ai = RandyAI()
        self.randy_ai.db_path = Path(self.test_db_path)
        self.randy_ai.init_database()
        
        self.scheduler = AutonomousScheduler(self.randy_ai)
        
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        os.rmdir(self.temp_dir)
        
    def test_daily_update_generation(self):
        """Test autonomous daily update generation"""
        # Add some test data
        self.randy_ai.create_task("High Priority Task", "Important task", 9)
        self.randy_ai.learn_from_interaction("test", "response", 0.8)
        
        # Generate daily update
        self.scheduler.generate_daily_update()
        
        # Check if update was saved
        timestamp = datetime.now().strftime('%Y%m%d')
        update_key = f"daily_update_{timestamp}"
        
        self.assertIn(update_key, self.randy_ai.memory)
        
    def test_improvement_area_identification(self):
        """Test self-improvement area identification"""
        areas = self.scheduler.identify_improvement_areas()
        
        self.assertIsInstance(areas, list)
        
        # Each area should have required fields
        for area in areas:
            self.assertIn('title', area)
            self.assertIn('description', area)
            self.assertIn('priority', area)
            
    def test_learning_recommendations(self):
        """Test learning recommendation generation"""
        # Test low success rate
        low_recommendations = self.scheduler.generate_learning_recommendations(0.5)
        self.assertGreater(len(low_recommendations), 0)
        self.assertTrue(any('simpler tasks' in rec.lower() for rec in low_recommendations))
        
        # Test high success rate
        high_recommendations = self.scheduler.generate_learning_recommendations(0.9)
        self.assertGreater(len(high_recommendations), 0)
        self.assertTrue(any('complex challenges' in rec.lower() for rec in high_recommendations))
        
    def test_schedule_status(self):
        """Test schedule status reporting"""
        status = self.scheduler.get_schedule_status()
        
        self.assertIsInstance(status, dict)
        self.assertIn('running', status)
        self.assertIn('scheduled_jobs', status)
        self.assertIn('custom_tasks', status)
        
    def test_reminder_creation(self):
        """Test reminder creation"""
        title = "Test Reminder"
        message = "This is a test reminder"
        reminder_time = datetime.now() + timedelta(hours=1)
        
        result = self.scheduler.create_reminder(title, message, reminder_time)
        
        self.assertIsInstance(result, str)
        self.assertIn("Reminder set", result)
        
class TestQuestionGenerator(unittest.TestCase):
    """Test question generation functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, "test_questions.db")
        
        self.randy_ai = RandyAI()
        self.randy_ai.db_path = Path(self.test_db_path)
        self.randy_ai.init_database()
        
        self.question_gen = QuestionGenerator(self.randy_ai)
        
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        os.rmdir(self.temp_dir)
        
    def test_contextual_question_generation(self):
        """Test contextual question generation"""
        # Add some context to memory
        self.randy_ai.save_memory("recent_car_search", "Toyota Corolla modifications", "search")
        
        question = self.question_gen.generate_contextual_question()
        
        self.assertIsInstance(question, str)
        self.assertGreater(len(question), 10)  # Should be a meaningful question
        self.assertTrue(question.endswith('?'))  # Should end with question mark
        
    def test_question_templates(self):
        """Test question template system"""
        templates = self.question_gen.question_templates
        
        self.assertIsInstance(templates, list)
        self.assertGreater(len(templates), 0)
        
        # All templates should contain placeholders
        for template in templates:
            self.assertTrue('{' in template and '}' in template)
            
class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def setUp(self):
        """Set up integration test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, "test_integration.db")
        
        # Initialize complete system
        self.randy_ai = RandyAI()
        self.randy_ai.db_path = Path(self.test_db_path)
        self.randy_ai.init_database()
        
        self.enhanced_ai = EnhancedRandyAI(self.randy_ai)
        self.scheduler = AutonomousScheduler(self.randy_ai)
        self.question_gen = QuestionGenerator(self.randy_ai)
        
    def tearDown(self):
        """Clean up integration test environment"""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        os.rmdir(self.temp_dir)
        
    def test_complete_workflow(self):
        """Test complete AI workflow"""
        # 1. Save user preferences and context
        self.randy_ai.save_memory("user_project", "AI assistant development", "projects")
        
        # 2. Create tasks
        task_id = self.randy_ai.create_task("Test AI Integration", "Complete integration testing", 8)
        self.assertIsInstance(task_id, int)
        
        # 3. Learn from interaction
        self.randy_ai.learn_from_interaction(
            "How to test AI integration?",
            "Use comprehensive test suite with unit and integration tests",
            0.9
        )
        
        # 4. Generate autonomous insights
        insights = self.scheduler.generate_autonomous_insights()
        self.assertIsInstance(insights, str)
        
        # 5. Create space configuration
        space_config = self.enhanced_ai.integrator.create_space_config(
            "TestSpace", "technical_assistant", "Integration testing"
        )
        self.assertIsInstance(space_config, dict)
        
        # 6. Generate contextual question
        question = self.question_gen.generate_contextual_question()
        self.assertIsInstance(question, str)
        
        # 7. Generate system status
        status = self.randy_ai.get_status()
        self.assertIn('memory_items', status)
        self.assertGreater(status['memory_items'], 0)
        
    def test_data_persistence(self):
        """Test data persistence across sessions"""
        # Create and save data
        test_memory_key = "persistence_test"
        test_memory_value = {"test": True, "timestamp": datetime.now().isoformat()}
        
        self.randy_ai.save_memory(test_memory_key, test_memory_value, "test")
        
        # Create new instance (simulating restart)
        new_randy_ai = RandyAI()
        new_randy_ai.db_path = Path(self.test_db_path)
        new_randy_ai.load_memory()
        
        # Verify data persistence
        self.assertIn(test_memory_key, new_randy_ai.memory)
        self.assertEqual(new_randy_ai.memory[test_memory_key], test_memory_value)
        
if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestRandyAICore,
        TestMultiPlatformIntegrator,
        TestAutonomousScheduler,
        TestQuestionGenerator,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
            
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
            
    # Exit with proper code
    exit_code = 0 if result.wasSuccessful() else 1
    sys.exit(exit_code)