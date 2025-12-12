# QUESTION 3 (PART 2) (PYTHON)
# DBS Admission Client - Student Application Form
# Collects info and sends to server

import socket
import json

class DBSAdmissionClient:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        # course options
        self.courses = {
            '1': 'MSc in Cyber Security',
            '2': 'MSc Information Systems & computing',
            '3': 'MSc Data Analytics'
        }
        self.months = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
    
    def display_banner(self):
        print("\n" + "="*60)
        print(" "*15 + "DBS ADMISSION SYSTEM")
        print("="*60)
        print("\nAvailable Courses:")
        for key, course in self.courses.items():
            print(f"{key}. {course}")
        print("="*60 + "\n")
    
    def get_input(self, prompt, validator=None):
        """Generic input function with validation"""
        while True:
            value = input(prompt).strip()
            if not validator or validator(value):
                return value
            print("Invalid input. Please try again.")
    
    def get_applicant_info(self):
        print("\n--- APPLICANT INFORMATION ---\n")
        
        # Get basic info
        name = self.get_input("Full Name: ", lambda x: x)
        address = self.get_input("Address: ", lambda x: x)
        qualifications = self.get_input("Educational Qualifications: ", lambda x: x)
        
        # Get course
        course_choice = self.get_input("Select course (1-3): ", lambda x: x in self.courses)
        course = self.courses[course_choice]
        
        # Get year
        start_year = int(self.get_input("Intended Start Year (e.g., 2025): ", 
                                        lambda x: x.isdigit() and 2024 <= int(x) <= 2030))
        
        # Get month
        print("\nMonths:")
        for i, month in enumerate(self.months, 1):
            print(f"{i}. {month}")
        
        month_idx = int(self.get_input("Select start month (1-12): ", 
                                       lambda x: x.isdigit() and 1 <= int(x) <= 12)) - 1
        
        return {
            'name': name,
            'address': address,
            'educational_qualifications': qualifications,
            'course': course,
            'start_year': start_year,
            'start_month': self.months[month_idx]
        }
    
    def display_summary(self, data):
        print("\n" + "="*60)
        print(" "*15 + "APPLICATION SUMMARY")
        print("="*60)
        print(f"Name: {data['name']}")
        print(f"Address: {data['address']}")
        print(f"Qualifications: {data['educational_qualifications']}")
        print(f"Course: {data['course']}")
        print(f"Start Date: {data['start_month']} {data['start_year']}")
        print("="*60)
    
    def submit_application(self, data):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"\n[CLIENT] Connecting to {self.host}:{self.port}...")
            client_socket.connect((self.host, self.port))
            print("[CLIENT] Connected!")
            
            # Send data
            client_socket.send(json.dumps(data).encode('utf-8'))
            print("[CLIENT] Application sent...")
            
            # Receive response
            response = json.loads(client_socket.recv(4096).decode('utf-8'))
            
            # Display result
            print("\n" + "="*60)
            if response['status'] == 'success':
                print(" "*15 + "APPLICATION SUCCESSFUL!")
                print("="*60)
                print(f"\nYour Registration Number: {response['registration_number']}")
                print("\nPlease save this registration number for future reference.")
            else:
                print(" "*20 + "APPLICATION FAILED")
                print("="*60)
                print(f"\nError: {response['message']}")
            print("="*60 + "\n")
            
            client_socket.close()
            return response
            
        except ConnectionRefusedError:
            print("\n[ERROR] Unable to connect. Ensure server is running.")
        except Exception as e:
            print(f"\n[ERROR] Something went wrong: {e}")
            # maybe check if server is running?
        return None
    
    def run(self):
        self.display_banner()
        data = self.get_applicant_info()
        self.display_summary(data)
        
        if input("\nSubmit application? (yes/no): ").strip().lower() in ['yes', 'y']:
            self.submit_application(data)
        else:
            print("\nApplication cancelled.")

if __name__ == "__main__":
    DBSAdmissionClient().run()