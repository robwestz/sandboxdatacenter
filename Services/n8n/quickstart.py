"""
n8n Integration - Workflow Automation
Connect to n8n instance for workflow orchestration
"""

import asyncio
import aiohttp
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json

@dataclass
class N8NConfig:
    """n8n connection configuration"""
    base_url: str = "http://localhost:5678"
    api_key: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

class N8NClient:
    """Client for interacting with n8n workflows"""

    def __init__(self, config: N8NConfig = None):
        self.config = config or N8NConfig()
        self.session = None
        self.headers = {}

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        if self.config.api_key:
            self.headers = {"X-N8N-API-KEY": self.config.api_key}
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def get_workflows(self) -> List[Dict]:
        """Get all workflows"""
        async with self.session.get(
            f"{self.config.base_url}/api/v1/workflows",
            headers=self.headers
        ) as response:
            return await response.json()

    async def execute_workflow(self,
                              workflow_id: str,
                              data: Dict = None) -> Dict:
        """Execute a workflow with optional data"""
        endpoint = f"{self.config.base_url}/api/v1/workflows/{workflow_id}/execute"

        async with self.session.post(
            endpoint,
            json={"data": data} if data else {},
            headers=self.headers
        ) as response:
            return await response.json()

    async def create_workflow(self, workflow_definition: Dict) -> Dict:
        """Create a new workflow"""
        async with self.session.post(
            f"{self.config.base_url}/api/v1/workflows",
            json=workflow_definition,
            headers=self.headers
        ) as response:
            return await response.json()

    async def trigger_webhook(self,
                            webhook_path: str,
                            data: Dict,
                            method: str = "POST") -> Dict:
        """Trigger a webhook workflow"""
        webhook_url = f"{self.config.base_url}/webhook/{webhook_path}"

        async with self.session.request(
            method,
            webhook_url,
            json=data
        ) as response:
            return await response.json()

# ============================================================
# WORKFLOW TEMPLATES
# ============================================================

def create_data_pipeline_workflow() -> Dict:
    """Template: Data processing pipeline"""
    return {
        "name": "Data Processing Pipeline",
        "nodes": [
            {
                "id": "webhook",
                "type": "n8n-nodes-base.webhook",
                "position": [250, 300],
                "parameters": {
                    "path": "process-data",
                    "responseMode": "onReceived",
                    "responseData": "allEntries"
                }
            },
            {
                "id": "transform",
                "type": "n8n-nodes-base.set",
                "position": [450, 300],
                "parameters": {
                    "values": {
                        "string": [{
                            "name": "processed",
                            "value": "={{$json.data}}"
                        }]
                    }
                }
            },
            {
                "id": "store",
                "type": "n8n-nodes-base.postgres",
                "position": [650, 300],
                "parameters": {
                    "operation": "insert",
                    "table": "processed_data"
                }
            }
        ],
        "connections": {
            "webhook": {
                "main": [["transform"]]
            },
            "transform": {
                "main": [["store"]]
            }
        }
    }

def create_notification_workflow() -> Dict:
    """Template: Multi-channel notification"""
    return {
        "name": "Multi-Channel Notifier",
        "nodes": [
            {
                "id": "trigger",
                "type": "n8n-nodes-base.webhook",
                "parameters": {
                    "path": "notify",
                    "responseMode": "onReceived"
                }
            },
            {
                "id": "email",
                "type": "n8n-nodes-base.emailSend",
                "parameters": {
                    "toEmail": "={{$json.email}}",
                    "subject": "{{$json.subject}}",
                    "text": "={{$json.message}}"
                }
            },
            {
                "id": "slack",
                "type": "n8n-nodes-base.slack",
                "parameters": {
                    "channel": "#notifications",
                    "text": "={{$json.message}}"
                }
            }
        ]
    }

# ============================================================
# INTEGRATION WITH NEURAL DATABASE
# ============================================================

async def track_workflow_execution(workflow_name: str,
                                  success: bool,
                                  execution_time: float):
    """Track workflow execution in Neural Database"""
    from neural_db import NeuralMemoryManager

    memory = NeuralMemoryManager()
    await memory.initialize()

    await memory.remember(
        f"n8n_workflow_{workflow_name}",
        {
            "workflow": workflow_name,
            "success": success,
            "execution_time": execution_time,
            "timestamp": str(asyncio.get_event_loop().time())
        },
        pattern_type="automation"
    )

    await memory.shutdown()

# ============================================================
# USAGE EXAMPLES
# ============================================================

async def example_basic_usage():
    """Basic n8n integration example"""

    # Configure client
    config = N8NConfig(
        base_url="http://localhost:5678"
        # api_key="your-api-key"  # If authentication is enabled
    )

    async with N8NClient(config) as client:
        # Get all workflows
        workflows = await client.get_workflows()
        print(f"Found {len(workflows)} workflows")

        # Execute a workflow
        result = await client.execute_workflow(
            workflow_id="workflow-123",
            data={"input": "test data"}
        )
        print(f"Execution result: {result}")

        # Trigger webhook
        webhook_result = await client.trigger_webhook(
            webhook_path="my-webhook",
            data={"message": "Hello from Python!"}
        )
        print(f"Webhook triggered: {webhook_result}")

async def example_create_automation():
    """Create a new automation workflow"""

    async with N8NClient() as client:
        # Create data pipeline
        pipeline = await client.create_workflow(
            create_data_pipeline_workflow()
        )
        print(f"Created pipeline: {pipeline['id']}")

        # Create notifier
        notifier = await client.create_workflow(
            create_notification_workflow()
        )
        print(f"Created notifier: {notifier['id']}")

async def example_orchestrate_with_sovereign():
    """Integrate n8n with SOVEREIGN agents"""

    async with N8NClient() as n8n:
        # SOVEREIGN agent triggers n8n workflow
        result = await n8n.trigger_webhook(
            webhook_path="sovereign-task",
            data={
                "agent": "DataProcessor",
                "task": "process_batch",
                "data": [1, 2, 3, 4, 5]
            }
        )

        # Track in Neural Database
        await track_workflow_execution(
            "sovereign-task",
            success=result.get("success", False),
            execution_time=result.get("executionTime", 0)
        )

if __name__ == "__main__":
    # Run examples
    asyncio.run(example_basic_usage())
    # asyncio.run(example_create_automation())
    # asyncio.run(example_orchestrate_with_sovereign())