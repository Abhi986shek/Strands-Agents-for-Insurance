"""
Flask routes for AutoGuard Insurance Agent
Handles web endpoints and session management
"""
import json
import uuid
import logging
from datetime import datetime
from flask import request, jsonify
from strands.session.file_session_manager import FileSessionManager
from .agent import create_agent, system_instructions

logger = logging.getLogger(__name__)

def setup_routes(app):
    @app.route('/insurance_bot/converse', methods=['POST'])
    def converse():
        """Flask endpoint for conversational interface"""
        try:
            data = request.get_json() or {}
            input_text = data.get('input_text', '').strip()
            if not input_text:
                return jsonify({"error": "input_text is required"}), 400

            # Generate or use provided session ID
            session_id = data.get('session_id') or str(uuid.uuid4())

            # Create isolated FileSessionManager per session
            session_manager = FileSessionManager(session_id=session_id)

            # Create a new agent for this session
            agent = create_agent(session_manager)

            # Add timestamp context
            input_text = f"{input_text} (Current datetime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"

            # Prepend system instructions
            full_message = f"{system_instructions}\n\nUser: {input_text}"

            # Get response
            agent_result = agent(full_message)
            response_text = str(agent_result)

            return jsonify({
                "response": response_text,
                "session_id": session_id,
                "status": "success"
            })

        except Exception as e:
            logger.error(f"Error in converse endpoint: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @app.route('/insurance_bot/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({"status": "healthy", "service": "AutoGuard Insurance Agent"})