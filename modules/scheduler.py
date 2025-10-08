"""
Scheduler Module for AURA Assistant
Handles task scheduling and automation
"""

import schedule
import time
import threading
import logging
import json
from datetime import datetime, timedelta
from pathlib import Path

class TaskScheduler:
    """Handles scheduled tasks and automation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.scheduler_thread = None
        self.tasks_file = Path("data/scheduled_tasks.json")
        self.tasks = {}
        self.load_tasks()
    
    def load_tasks(self):
        """Load scheduled tasks from file"""
        try:
            if self.tasks_file.exists():
                with open(self.tasks_file, 'r') as f:
                    self.tasks = json.load(f)
                self.logger.info(f"Loaded {len(self.tasks)} scheduled tasks")
            else:
                self.tasks = {}
                
        except Exception as e:
            self.logger.error(f"Failed to load tasks: {e}")
            self.tasks = {}
    
    def save_tasks(self):
        """Save scheduled tasks to file"""
        try:
            self.tasks_file.parent.mkdir(exist_ok=True)
            with open(self.tasks_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
            self.logger.info("Tasks saved successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to save tasks: {e}")
    
    def add_task(self, task_id, task_type, schedule_time, command, description=""):
        """Add a new scheduled task"""
        try:
            task = {
                'id': task_id,
                'type': task_type,  # 'daily', 'weekly', 'once', 'interval'
                'schedule_time': schedule_time,
                'command': command,
                'description': description,
                'created': datetime.now().isoformat(),
                'active': True
            }
            
            self.tasks[task_id] = task
            self.save_tasks()
            self.schedule_task(task)
            
            self.logger.info(f"Task '{task_id}' added successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add task: {e}")
            return False
    
    def remove_task(self, task_id):
        """Remove a scheduled task"""
        try:
            if task_id in self.tasks:
                # Cancel the scheduled job
                schedule.cancel_job(task_id)
                del self.tasks[task_id]
                self.save_tasks()
                
                self.logger.info(f"Task '{task_id}' removed successfully")
                return True
            else:
                self.logger.error(f"Task '{task_id}' not found")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to remove task: {e}")
            return False
    
    def schedule_task(self, task):
        """Schedule a task with the schedule library"""
        try:
            task_id = task['id']
            task_type = task['type']
            schedule_time = task['schedule_time']
            command = task['command']
            
            if task_type == 'daily':
                schedule.every().day.at(schedule_time).do(
                    self.execute_task, command
                ).tag(task_id)
                
            elif task_type == 'weekly':
                # schedule_time format: "monday 09:00"
                day, time_str = schedule_time.split(' ')
                getattr(schedule.every(), day.lower()).at(time_str).do(
                    self.execute_task, command
                ).tag(task_id)
                
            elif task_type == 'interval':
                # schedule_time format: "30" (minutes)
                interval = int(schedule_time)
                schedule.every(interval).minutes.do(
                    self.execute_task, command
                ).tag(task_id)
                
            elif task_type == 'once':
                # For one-time tasks, we'll check in run_pending
                pass
            
            self.logger.info(f"Task '{task_id}' scheduled successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to schedule task: {e}")
    
    def execute_task(self, command):
        """Execute a scheduled task command"""
        try:
            self.logger.info(f"Executing scheduled command: {command}")
            
            # Import here to avoid circular imports
            from modules.command_handler import CommandHandler
            
            command_handler = CommandHandler()
            result = command_handler.handle_command(command)
            
            self.logger.info(f"Scheduled task completed: {result}")
            
        except Exception as e:
            self.logger.error(f"Task execution failed: {e}")
    
    def start_scheduler(self):
        """Start the task scheduler"""
        try:
            if self.running:
                return
            
            self.running = True
            
            # Schedule all existing tasks
            for task in self.tasks.values():
                if task.get('active', True):
                    self.schedule_task(task)
            
            # Start scheduler thread
            self.scheduler_thread = threading.Thread(target=self.run_scheduler)
            self.scheduler_thread.daemon = True
            self.scheduler_thread.start()
            
            self.logger.info("Task scheduler started")
            
        except Exception as e:
            self.logger.error(f"Failed to start scheduler: {e}")
    
    def stop_scheduler(self):
        """Stop the task scheduler"""
        try:
            self.running = False
            schedule.clear()
            
            if self.scheduler_thread:
                self.scheduler_thread.join(timeout=5)
            
            self.logger.info("Task scheduler stopped")
            
        except Exception as e:
            self.logger.error(f"Failed to stop scheduler: {e}")
    
    def run_scheduler(self):
        """Main scheduler loop"""
        while self.running:
            try:
                schedule.run_pending()
                self.check_one_time_tasks()
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Scheduler loop error: {e}")
                time.sleep(60)
    
    def check_one_time_tasks(self):
        """Check and execute one-time tasks"""
        try:
            current_time = datetime.now()
            
            for task_id, task in list(self.tasks.items()):
                if task['type'] == 'once' and task.get('active', True):
                    scheduled_time = datetime.fromisoformat(task['schedule_time'])
                    
                    if current_time >= scheduled_time:
                        self.execute_task(task['command'])
                        # Mark task as completed
                        task['active'] = False
                        task['completed'] = current_time.isoformat()
                        self.save_tasks()
                        
        except Exception as e:
            self.logger.error(f"One-time task check failed: {e}")
    
    def list_tasks(self):
        """List all scheduled tasks"""
        return self.tasks
    
    def get_task(self, task_id):
        """Get specific task details"""
        return self.tasks.get(task_id)
    
    def toggle_task(self, task_id):
        """Enable/disable a task"""
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task['active'] = not task.get('active', True)
                
                if task['active']:
                    self.schedule_task(task)
                else:
                    schedule.cancel_job(task_id)
                
                self.save_tasks()
                
                status = "enabled" if task['active'] else "disabled"
                self.logger.info(f"Task '{task_id}' {status}")
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to toggle task: {e}")
            return False
    
    def add_reminder(self, reminder_text, when):
        """Add a reminder task"""
        try:
            task_id = f"reminder_{int(time.time())}"
            command = f"speak {reminder_text}"
            
            # Parse 'when' parameter
            if 'minute' in when:
                minutes = int(when.split()[0])
                schedule_time = (datetime.now() + timedelta(minutes=minutes)).isoformat()
                task_type = 'once'
            elif 'hour' in when:
                hours = int(when.split()[0])
                schedule_time = (datetime.now() + timedelta(hours=hours)).isoformat()
                task_type = 'once'
            elif ':' in when:  # Time format like "14:30"
                schedule_time = when
                task_type = 'daily'
            else:
                return False
            
            return self.add_task(
                task_id, 
                task_type, 
                schedule_time, 
                command, 
                f"Reminder: {reminder_text}"
            )
            
        except Exception as e:
            self.logger.error(f"Failed to add reminder: {e}")
            return False
    
    def get_next_tasks(self, count=5):
        """Get next scheduled tasks"""
        try:
            upcoming = []
            current_time = datetime.now()
            
            for task in self.tasks.values():
                if not task.get('active', True):
                    continue
                
                if task['type'] == 'once':
                    scheduled_time = datetime.fromisoformat(task['schedule_time'])
                    if scheduled_time > current_time:
                        upcoming.append({
                            'id': task['id'],
                            'description': task.get('description', task['command']),
                            'time': scheduled_time.strftime('%Y-%m-%d %H:%M'),
                            'type': 'once'
                        })
                elif task['type'] == 'daily':
                    upcoming.append({
                        'id': task['id'],
                        'description': task.get('description', task['command']),
                        'time': f"Daily at {task['schedule_time']}",
                        'type': 'daily'
                    })
            
            # Sort by time and return top count
            upcoming.sort(key=lambda x: x['time'])
            return upcoming[:count]
            
        except Exception as e:
            self.logger.error(f"Failed to get next tasks: {e}")
            return []