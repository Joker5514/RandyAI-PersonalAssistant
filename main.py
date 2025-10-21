#!/usr/bin/env python3
"""
RandyAI Personal Assistant - Main Application
Complete autonomous AI system for Randy Jordan

Usage:
    python main.py --start          # Start the AI system
    python main.py --status         # Check system status
    python main.py --config         # Configure API keys
    python main.py --update         # Force daily update
    python main.py --interactive    # Interactive mode
"""

import asyncio
import argparse
import json
from datetime import datetime
import sys
from pathlib import Path

# Import our modules
sys.path.append(str(Path(__file__).parent))
from core.randy_ai import RandyAI
from integrations.multi_platform import EnhancedRandyAI, MultiPlatformIntegrator
from autonomous.scheduler import AutonomousScheduler, QuestionGenerator

class RandyAISystem:
    """Main RandyAI system controller"""
    
    def __init__(self):
        print("🤖 Initializing RandyAI Personal Assistant...")
        
        # Initialize core components
        self.core_ai = RandyAI()
        self.enhanced_ai = EnhancedRandyAI(self.core_ai)
        self.scheduler = AutonomousScheduler(self.core_ai)
        self.question_gen = QuestionGenerator(self.core_ai)
        
        print("✅ RandyAI System Initialized")
        
    def configure_apis(self):
        """Interactive API configuration"""
        print("\n🔧 API Configuration")
        print("="*50)
        
        apis = {
            'perplexity': 'Perplexity API Key',
            'abacus': 'Abacus.AI API Key',
            'deepagent': 'DeepAgent API Key',
            'github': 'GitHub Personal Access Token'
        }
        
        for api_name, description in apis.items():
            current_key = self.core_ai.memory.get(f"api_key_{api_name}", "Not configured")
            print(f"\n{description}: {'✅ Configured' if current_key != 'Not configured' else '❌ Missing'}")
            
            if input(f"Update {api_name} API key? (y/N): ").lower() == 'y':
                new_key = input(f"Enter {description}: ").strip()
                if new_key:
                    self.enhanced_ai.integrator.configure_api(api_name, new_key)
                    print(f"✅ {description} updated")
                    
        print("\n🔧 Configuration complete!")
        
    def display_status(self):
        """Display comprehensive system status"""
        print("\n📊 RandyAI System Status")
        print("="*50)
        
        # Core system status
        core_status = self.core_ai.get_status()
        print(f"Memory Items: {core_status['memory_items']}")
        print(f"Learning Items: {core_status['learning_items']}")
        print(f"Pending Tasks: {core_status['pending_tasks']}")
        print(f"Last Update: {core_status['last_update']}")
        
        # Integration status
        integration_status = self.enhanced_ai.integrator.get_integration_status()
        print("\n🔗 Integration Status:")
        for platform, status in integration_status.items():
            configured = "✅" if status['configured'] else "❌"
            active = "🟢" if status['active'] else "🔴"
            print(f"  {platform.title()}: {configured} {active}")
            
        # Scheduler status
        scheduler_status = self.scheduler.get_schedule_status()
        print(f"\n⏰ Scheduler: {'🟢 Running' if scheduler_status['running'] else '🔴 Stopped'}")
        print(f"Scheduled Jobs: {scheduler_status['scheduled_jobs']}")
        print(f"Next Run: {scheduler_status['next_run']}")
        
        # Recent tasks
        recent_tasks = self.core_ai.get_pending_tasks()[:5]
        if recent_tasks:
            print("\n📋 Recent Tasks:")
            for task in recent_tasks:
                priority_emoji = "🔥" if task['priority'] >= 8 else "⭐" if task['priority'] >= 6 else "📌"
                print(f"  {priority_emoji} {task['title']} (Priority: {task['priority']})")
                
    async def interactive_mode(self):
        """Interactive conversation mode"""
        print("\n💬 Interactive Mode - Chat with RandyAI")
        print("Type 'exit' to quit, 'status' for system status, 'help' for commands")
        print("="*60)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() == 'exit':
                    break
                elif user_input.lower() == 'status':
                    self.display_status()
                    continue
                elif user_input.lower() == 'help':
                    self.show_interactive_help()
                    continue
                elif user_input.lower().startswith('task'):
                    self.handle_task_command(user_input)
                    continue
                elif user_input.lower().startswith('memory'):
                    self.handle_memory_command(user_input)
                    continue
                    
                if user_input:
                    print("\nRandyAI: Processing your request...")
                    
                    # Use enhanced AI for response
                    response = await self.enhanced_ai.enhanced_query(user_input)
                    print(f"\nRandyAI: {response}")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                
    def show_interactive_help(self):
        """Show available interactive commands"""
        help_text = """
        🔧 Available Commands:
        
        Basic:
          exit                 - Quit interactive mode
          status               - Show system status
          help                 - Show this help
          
        Tasks:
          task list            - List pending tasks
          task create <title>  - Create new task
          task complete <id>   - Mark task as complete
          
        Memory:
          memory list          - List recent memory items
          memory save <key> <value> - Save to memory
          memory get <key>     - Retrieve memory item
          
        System:
          update               - Force daily update
          learn <input> <output> - Add learning data
          
        Just type naturally for AI responses!
        """
        print(help_text)
        
    def handle_task_command(self, command: str):
        """Handle task-related commands"""
        parts = command.split(maxsplit=2)
        
        if len(parts) < 2:
            print("Usage: task [list|create|complete] [arguments]")
            return
            
        action = parts[1].lower()
        
        if action == 'list':
            tasks = self.core_ai.get_pending_tasks()[:10]
            if tasks:
                print("\n📋 Pending Tasks:")
                for i, task in enumerate(tasks):
                    print(f"  {i+1}. {task['title']} (Priority: {task['priority']})")
            else:
                print("\n✅ No pending tasks!")
                
        elif action == 'create' and len(parts) > 2:
            title = parts[2]
            task_id = self.core_ai.create_task(title, "", 5)
            print(f"✅ Task created with ID: {task_id}")
            
        else:
            print("Usage: task [list|create <title>]")
            
    def handle_memory_command(self, command: str):
        """Handle memory-related commands"""
        parts = command.split(maxsplit=3)
        
        if len(parts) < 2:
            print("Usage: memory [list|save|get] [arguments]")
            return
            
        action = parts[1].lower()
        
        if action == 'list':
            recent_memory = list(self.core_ai.memory.items())[-10:]
            if recent_memory:
                print("\n🧠 Recent Memory:")
                for key, value in recent_memory:
                    value_str = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                    print(f"  {key}: {value_str}")
            else:
                print("\n💭 No memory items found")
                
        elif action == 'save' and len(parts) > 3:
            key, value = parts[2], parts[3]
            self.core_ai.save_memory(key, value, "user_input")
            print(f"✅ Saved to memory: {key}")
            
        elif action == 'get' and len(parts) > 2:
            key = parts[2]
            value = self.core_ai.memory.get(key, "Not found")
            print(f"Memory [{key}]: {value}")
            
        else:
            print("Usage: memory [list|save <key> <value>|get <key>]")
            
    async def start_autonomous_mode(self):
        """Start full autonomous operation"""
        print("\n🚀 Starting Autonomous Mode...")
        
        # Start all autonomous components
        tasks = [
            self.scheduler.start_autonomous_scheduler(),
            self.question_gen.autonomous_question_cycle(),
            self.enhanced_ai.start_autonomous_mode()
        ]
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print("\n🛑 Stopping autonomous mode...")
            self.scheduler.stop_scheduler()
        except Exception as e:
            print(f"\n❌ Autonomous mode error: {str(e)}")
            
    def force_daily_update(self):
        """Force generate daily update"""
        print("\n📊 Generating Daily Update...")
        
        update = self.core_ai.daily_update()
        print(update)
        
        # Save the update
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.core_ai.save_memory(f"manual_update_{timestamp}", update, "reports")
        
        print("\n✅ Daily update saved to memory")
        
    def show_welcome(self):
        """Show welcome message with system info"""
        welcome = f"""
        🤖 RandyAI Personal Assistant
        =======================================
        
        👋 Welcome Randy!
        
        Your personal AI is ready with:
        ✅ Autonomous learning and adaptation
        ✅ Multi-platform integration (Perplexity, Abacus.AI, DeepAgent)
        ✅ Daily updates and self-improvement
        ✅ Task management and reminders
        ✅ Persistent memory and pattern recognition
        ✅ GitHub integration and project tracking
        
        Location: {self.core_ai.preferences.location}
        Vehicle: {self.core_ai.preferences.vehicle}
        Work: {', '.join(self.core_ai.preferences.work)}
        
        System initialized: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Use --help to see available commands
        """
        print(welcome)
        
async def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description='RandyAI Personal Assistant')
    parser.add_argument('--start', action='store_true', help='Start autonomous mode')
    parser.add_argument('--status', action='store_true', help='Show system status')
    parser.add_argument('--config', action='store_true', help='Configure API keys')
    parser.add_argument('--update', action='store_true', help='Force daily update')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--welcome', action='store_true', help='Show welcome message')
    
    args = parser.parse_args()
    
    # Initialize system
    randy_system = RandyAISystem()
    
    if args.welcome or len(sys.argv) == 1:
        randy_system.show_welcome()
    elif args.config:
        randy_system.configure_apis()
    elif args.status:
        randy_system.display_status()
    elif args.update:
        randy_system.force_daily_update()
    elif args.interactive:
        await randy_system.interactive_mode()
    elif args.start:
        await randy_system.start_autonomous_mode()
    else:
        parser.print_help()
        
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 RandyAI shutting down gracefully...")
    except Exception as e:
        print(f"\n❌ System error: {str(e)}")
        sys.exit(1)