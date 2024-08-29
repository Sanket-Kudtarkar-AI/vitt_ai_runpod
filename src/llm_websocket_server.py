from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from llm_token_streaming import function_stream
import eventlet

app = Flask(__name__)
sockio = SocketIO(app, cors_allowed_origins="*")


@app.route('/get_llm_response', methods=['GET', 'POST'])
def get_llm_response():
    try:
        req = request.get_json()
        query = req.get('query')
        if not query:
            return jsonify({"status": "error", "message": "Query parameter is missing"}), 400

        llm_response = function_stream(None, sessionid=None, prompt=query, stream=False)
        return jsonify({"status": "success", "llm_response": llm_response})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error in : get_llm_response\n\n Error details: {str(e)}"}), 500


# @sockio.on('messagefromclient')
# def stream_llm_response(data):
#     sock_id = None
#     try:
#         sock_id = request.sid
#         query = data.get('query')
#         sessid = data.get('sessionid')
#
#         if not query:
#             emit('messagefromserver', {"status": "error", "message": "Query parameter is missing"}, room=sock_id)
#             return
#
#         function_stream(sock_id, sessid, query, stream=True)
#
#     except Exception as e:
#         error_message = {"status": "error", "message": f"Error in : stream_llm_response\n\n Error details: {str(e)}"}
#         if sock_id:
#             emit('messagefromserver', error_message, room=sock_id)
#         else:
#             emit('messagefromserver', error_message)


if __name__ == '__main__':
    sockio.run(app, debug=True, host="0.0.0.0", port=3008)
