import json
import logging
import boto3
from typing import Dict, List
from strands import tool
from botocore.exceptions import ClientError, BotoCoreError

logger = logging.getLogger(__name__)

# Initialize Bedrock Agent Runtime client
try:
    bedrock_agent_runtime = boto3.client(
        'bedrock-agent-runtime',
        region_name='ap-south-1'  # Adjust region as needed
    )
except Exception as e:
    logger.error(f"Failed to initialize Bedrock client: {str(e)}")
    bedrock_agent_runtime = None

@tool
def query_knowledge_base(query: str, max_results: int = 5) -> Dict:
    """
    Queries the AutoGuard knowledge base to retrieve relevant information.
    Args:
        query: The question or search query to find information about
        max_results: Maximum number of results to return (default: 5)
    Returns:
        Dictionary with retrieved knowledge base information
    """
    if not bedrock_agent_runtime:
        return {
            "status": "error",
            "message": "Knowledge base service is not available",
            "results": []
        }

    if not query or not query.strip():
        return {
            "status": "error",
            "message": "Query cannot be empty",
            "results": []
        }

    try:
        logger.info(f"Querying knowledge base with: {query}")
        
        # Query the knowledge base
        response = bedrock_agent_runtime.retrieve(
            knowledgeBaseId='VEW79HHGF5',
            retrievalQuery={
                'text': query.strip()
            },
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': min(max_results, 20) 
                }
            }
        )

        # Process the results
        results = []
        for item in response.get('retrievalResults', []):
            content = item.get('content', {}).get('text', '')
            score = item.get('score', 0.0)
            location = item.get('location', {})
            
            # Extract source information
            source_info = {}
            if location.get('type') == 'S3':
                s3_location = location.get('s3Location', {})
                source_info = {
                    'type': 'document',
                    'bucket': s3_location.get('uri', '').split('/')[2] if '/' in s3_location.get('uri', '') else '',
                    'key': '/'.join(s3_location.get('uri', '').split('/')[3:]) if '/' in s3_location.get('uri', '') else ''
                }
            
            results.append({
                'content': content,
                'relevance_score': score,
                'source': source_info
            })

        logger.info(f"Knowledge base returned {len(results)} results")
        
        return {
            "status": "success",
            "message": f"Found {len(results)} relevant results",
            "results": results,
            "query": query
        }

    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_message = e.response.get('Error', {}).get('Message', str(e))
        
        logger.error(f"AWS ClientError querying knowledge base: {error_code} - {error_message}")       
        if error_code == 'ResourceNotFoundException':
            return {
                "status": "error",
                "message": "Knowledge base not found or not accessible",
                "results": []
            }
        elif error_code == 'AccessDeniedException':
            return {
                "status": "error", 
                "message": "Access denied to knowledge base",
                "results": []
            }
        else:
            return {
                "status": "error",
                "message": f"Knowledge base query failed: {error_message}",
                "results": []
            }

    except BotoCoreError as e:
        logger.error(f"BotoCoreError querying knowledge base: {str(e)}")
        return {
            "status": "error",
            "message": "Knowledge base service connection failed",
            "results": []
        }

    except Exception as e:
        logger.error(f"Unexpected error querying knowledge base: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": "An unexpected error occurred while searching knowledge base",
            "results": []
        }