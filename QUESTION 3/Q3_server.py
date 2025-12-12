# QUESTION 3 (PART 2) (PYTHON)
# DBS College Admission Server
# Stores student applications in SQLite and returns registration numbers

import socket
import sqlite3
import json
import hashlib
import secrets
from datetime import datetime
import threading

class DBSAdmissionServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect('dbs_applications.db')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                registration_number TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                educational_qualifications TEXT NOT NULL,
                course TEXT NOT NULL,
                start_year INTEGER NOT NULL,
                start_month TEXT NOT NULL,
                application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("[SERVER] Database initialized")
    
    def generate_registration_number(self, name, course):
        year = datetime.now().year
        # Course codes for different programs
        course_codes = {
            'MSc in Cyber Security': 'CS',
            'MSc Information Systems & computing': 'ISC',
            'MSc Data Analytics': 'DA'
        }
        
        course_code = course_codes.get(course, 'GEN')
        random_part = secrets.token_hex(4).upper()
        hash_part = hashlib.md5(f"{name}{course}{datetime.now().isoformat()}{random_part}".encode()).hexdigest()[:4].upper()
        
        return f"DBS-{year}-{course_code}-{hash_part}-{random_part}"
    
    def save_application(self, data):
        try:
            conn = sqlite3.connect('dbs_applications.db')
            reg_num = self.generate_registration_number(data['name'], data['course'])
            
            conn.execute('''
                INSERT INTO applications 
                (registration_number, name, address, educational_qualifications, 
                 course, start_year, start_month)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (reg_num, data['name'], data['address'], data['educational_qualifications'],
                  data['course'], data['start_year'], data['start_month']))
            
            conn.commit()
            conn.close()
            print(f"[SERVER] Saved: {reg_num}")
            return reg_num
            
        except sqlite3.IntegrityError:
            return self.save_application(data)
        except Exception as e:
            print(f"[SERVER] Error: {e}")
            return None
    
    def handle_client(self, client_socket, address):
        print(f"[SERVER] Connection from {address}")
        
        try:
            data = json.loads(client_socket.recv(4096).decode('utf-8'))
            print(f"[SERVER] Application from: {data['name']}")
            
            # Validate fields
            required = ['name', 'address', 'educational_qualifications', 'course', 'start_year', 'start_month']
            if not all(field in data for field in required):
                response = {'status': 'error', 'message': 'Missing required fields'}
            else:
                reg_num = self.save_application(data)
                if reg_num:
                    response = {'status': 'success', 'registration_number': reg_num, 'message': 'Success'}
                else:
                    response = {'status': 'error', 'message': 'Failed to process'}
            
            client_socket.send(json.dumps(response).encode('utf-8'))
            print(f"[SERVER] Response sent to {address}")
            
        except Exception as e:
            print(f"[SERVER] Error with {address}: {e}")
            client_socket.send(json.dumps({'status': 'error', 'message': 'Server error'}).encode('utf-8'))
        finally:
            client_socket.close()
            print(f"[SERVER] Closed connection with {address}")
    
    def start(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            
            print(f"[SERVER] Started on {self.host}:{self.port}")
            print("[SERVER] Waiting for connections...")
            
            while True:
                client_socket, address = server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, address)).start()
                
        except KeyboardInterrupt:
            print("\n[SERVER] Shutting down...")
        except Exception as e:
            print(f"[SERVER] Error: {e}")
        finally:
            server_socket.close()
            print("[SERVER] Stopped")

if __name__ == "__main__":
    DBSAdmissionServer().start()