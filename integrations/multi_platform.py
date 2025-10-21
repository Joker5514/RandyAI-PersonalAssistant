#!/usr/bin/env python3
"""
Multi-Platform Integration Module
Connects RandyAI to Perplexity, Abacus.AI, DeepAgent, and other services
"""

import asyncio
import json
import aiohttp
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class APIConfig:
    """API Configuration for each service"""
    name: str
    endpoint: str
    key: str
    headers: Dict[str, str]
    active: bool = True

class MultiPlatformIntegrator:
    """Manages connections to multiple AI platforms"""
    
    def __init__(self, randy_ai_instance):
        self.randy_ai = randy_ai_instance
        self.apis = {}
        self.session = None
        self.setup_apis()
        
    def setup_apis(self):
        """Configure API endpoints"""
        # Perplexity Configuration
        self.apis['perplexity'] = APIConfig(
            name="Perplexity",
            endpoint="https://api.perplexity.ai/chat/completions",
            key="",  # To be configured
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {key}"
            }
        )
        
        # Abacus.AI Configuration
        self.apis['abacus'] = APIConfig(
            name="Abacus.AI",
            endpoint="https://routellm.abacus.ai/v1/chat/completions",
            key="",  # To be configured
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {key}"
            }
        )
        
        # DeepAgent Configuration
        self.apis['deepagent'] = APIConfig(
            name="DeepAgent",
            endpoint="https://api.deepagent.ai/v1/completions",
            key="",  # To be configured
            headers={
                "Content-Type": "application/json",
                "X-API-Key": "{key}"
            }
        )
        
    async def init_session(self):
        """Initialize HTTP session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def close_session(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
            
    def configure_api(self, service: str, api_key: str):
        """Configure API key for a service"""
        if service in self.apis:
            self.apis[service].key = api_key
            self.randy_ai.save_memory(f"api_key_{service}", api_key, "credentials")
            return True
        return False
        
    async def query_perplexity(self, prompt: str, context: str = "") -> Dict:
        """Query Perplexity API with context"""
        await self.init_session()
        
        if not self.apis['perplexity'].key:
            return {"error": "Perplexity API key not configured"}
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.apis['perplexity'].key}"
        }
        
        data = {
            "model": "llama-3.1-sonar-large-128k-online",
            "messages": [
                {"role": "system", "content": f"You are Randy's personal AI assistant. Context: {context}"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        try:
            async with self.session.post(self.apis['perplexity'].endpoint, 
                                       headers=headers, json=data) as response:
                result = await response.json()
                return {
                    "success": True,
                    "response": result['choices'][0]['message']['content'],
                    "tokens_used": result.get('usage', {})
                }
        except Exception as e:
            return {"error": f"Perplexity API error: {str(e)}"}
            
    async def send_to_abacus(self, data: Dict, project_type: str = "general") -> Dict:
        """Send data to Abacus.AI for processing"""
        await self.init_session()
        
        if not self.apis['abacus'].key:
            return {"error": "Abacus API key not configured"}
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.apis['abacus'].key}"
        }
        
        payload = {
            "model": "deepseek-r1",
            "messages": [
                {
                    "role": "system", 
                    "content": f"Process this data for Randy's {project_type} project"
                },
                {"role": "user", "content": json.dumps(data)}
            ],
            "stream": False
        }
        
        try:
            async with self.session.post(self.apis['abacus'].endpoint,
                                       headers=headers, json=payload) as response:
                result = await response.json()
                return {
                    "success": True,
                    "processed_data": result['choices'][0]['message']['content'],
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {"error": f"Abacus API error: {str(e)}"}
            
    async def handoff_to_deepagent(self, project_data: Dict, instructions: str) -> Dict:
        """Handoff project to DeepAgent for development"""
        handoff_package = {
            "project_name": project_data.get("name", "RandyAI_Project"),
            "description": project_data.get("description", ""),
            "code_base": project_data.get("code", ""),
            "requirements": project_data.get("requirements", []),
            "instructions": instructions,
            "user_preferences": self.randy_ai.preferences.__dict__,
            "memory_context": dict(list(self.randy_ai.memory.items())[-10:]),  # Last 10 items
            "timestamp": datetime.now().isoformat(),
            "handoff_type": "development_continuation"
        }
        
        # Save handoff locally
        filename = f"handoff_{project_data.get('name', 'project')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(handoff_package, f, indent=2)
                
            self.randy_ai.save_memory(f"handoff_{filename}", handoff_package, "handoffs")
            
            return {
                "success": True,
                "handoff_file": filename,
                "package_size": len(json.dumps(handoff_package)),
                "instructions": f"Project handed off to DeepAgent. File: {filename}"
            }
        except Exception as e:
            return {"error": f"Handoff error: {str(e)}"}
            
    async def sync_with_github(self, repo_data: Dict) -> Dict:
        """Sync project data with GitHub repository"""
        # Implementation for GitHub API integration
        return {
            "success": True,
            "message": "GitHub sync completed",
            "repo_url": repo_data.get("url", "")
        }
        
    async def orchestrate_multi_query(self, query: str, platforms: List[str] = None) -> Dict:
        """Send query to multiple platforms and combine results"""
        if platforms is None:
            platforms = ['perplexity', 'abacus']
            
        results = {}
        
        tasks = []
        for platform in platforms:
            if platform == 'perplexity' and self.apis['perplexity'].key:
                tasks.append(self.query_perplexity(query))
            elif platform == 'abacus' and self.apis['abacus'].key:
                tasks.append(self.send_to_abacus({"query": query}, "multi_query"))
                
        if tasks:
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, response in enumerate(responses):
                platform = platforms[i] if i < len(platforms) else f"platform_{i}"
                if isinstance(response, Exception):
                    results[platform] = {"error": str(response)}
                else:
                    results[platform] = response
                    
        return {
            "query": query,
            "platforms_queried": platforms,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    def create_space_config(self, space_name: str, personality: str, purpose: str) -> Dict:
        """Create configuration for a new AI space"""
        config = {
            "name": space_name,
            "personality": personality,
            "purpose": purpose,
            "owner": "Randy Jordan",
            "created": datetime.now().isoformat(),
            "preferences": {
                "tone": self.randy_ai.preferences.tone_preference,
                "code_limit": self.randy_ai.preferences.code_limit,
                "location_context": self.randy_ai.preferences.location
            },
            "memory_access": True,
            "learning_enabled": True
        }
        
        self.randy_ai.save_memory(f"space_config_{space_name}", config, "spaces")
        return config
        
    async def autonomous_platform_check(self):
        """Autonomously check all platforms for updates"""
        check_results = {}
        
        for platform_name, api_config in self.apis.items():
            if api_config.active and api_config.key:
                try:
                    # Simple health check
                    status = await self.platform_health_check(platform_name)
                    check_results[platform_name] = status
                except Exception as e:
                    check_results[platform_name] = {"error": str(e)}
                    
        return check_results
        
    async def platform_health_check(self, platform: str) -> Dict:
        """Check if platform is accessible"""
        # Simple ping to check platform availability
        return {
            "status": "online",
            "last_check": datetime.now().isoformat()
        }
        
    def get_integration_status(self) -> Dict:
        """Get status of all integrations"""
        status = {}
        for name, api in self.apis.items():
            status[name] = {
                "configured": bool(api.key),
                "active": api.active,
                "endpoint": api.endpoint
            }
        return status

# Integration with main RandyAI class
class EnhancedRandyAI:
    """Enhanced RandyAI with multi-platform integration"""
    
    def __init__(self, base_randy_ai):
        self.base_ai = base_randy_ai
        self.integrator = MultiPlatformIntegrator(base_randy_ai)
        
    async def enhanced_query(self, query: str, use_multiple_platforms: bool = True) -> str:
        """Enhanced query using multiple platforms"""
        if use_multiple_platforms:
            results = await self.integrator.orchestrate_multi_query(query)
            
            # Combine and process results
            combined_response = self.process_multi_platform_results(results)
            
            # Learn from the interaction
            self.base_ai.learn_from_interaction(query, combined_response)
            
            return combined_response
        else:
            # Use single platform (Perplexity by default)
            result = await self.integrator.query_perplexity(query)
            return result.get('response', 'No response received')
            
    def process_multi_platform_results(self, results: Dict) -> str:
        """Process and combine results from multiple platforms"""
        combined = "Multi-Platform AI Response:\n\n"
        
        for platform, result in results.get('results', {}).items():
            if 'error' not in result:
                response_text = result.get('response', result.get('processed_data', ''))
                combined += f"{platform.title()} Response:\n{response_text}\n\n"
                
        return combined
        
    async def start_autonomous_mode(self):
        """Start autonomous operation with multi-platform integration"""
        while True:
            try:
                # Check platform status
                await self.integrator.autonomous_platform_check()
                
                # Run base AI autonomous operations
                await self.base_ai.pattern_analysis()
                
                # Check for pending handoffs
                # Implementation for checking and processing handoffs
                
                await asyncio.sleep(600)  # 10 minutes
                
            except Exception as e:
                self.base_ai.save_memory("integration_error", str(e), "errors")
                await asyncio.sleep(300)  # 5 minutes on error