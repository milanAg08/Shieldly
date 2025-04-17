# backend/deploy.py

import os
import subprocess
import argparse

def run_command(command):
    """Run a shell command and print output"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def setup_environment():
    """Set up the environment variables"""
    if not os.path.exists('.env'):
        print("Creating .env file...")
        with open('.env', 'w') as f:
            f.write('FLASK_APP=backend.app\n')
            f.write('FLASK_ENV=production\n')
            f.write(f'SECRET_KEY={os.urandom(24).hex()}\n')
            f.write(f'ENCRYPTION_KEY={os.urandom(16).hex()}\n')
            f.write('DATABASE_URL=sqlite:///instance/shieldly_prod.db\n')
    else:
        print(".env file already exists. Skipping...")

def install_dependencies():
    """Install dependencies from requirements.txt"""
    return run_command("pip install -r requirements.txt")

def initialize_database():
    """Initialize the database"""
    if run_command("flask db init"):
        if run_command("flask db migrate -m 'Initial migration'"):
            return run_command("flask db upgrade")
    return False

def run_tests():
    """Run the test suite"""
    return run_command("python -m unittest discover -s tests")

def main():
    parser = argparse.ArgumentParser(description='Deploy the Shieldly backend')
    parser.add_argument('--skip-tests', action='store_true', help='Skip running tests')
    parser.add_argument('--skip-env', action='store_true', help='Skip environment setup')
    args = parser.parse_args()
    
    print("Starting deployment of Shieldly backend...")
    
    if not args.skip_env:
        setup_environment()
    
    if not install_dependencies():
        print("Failed to install dependencies. Aborting.")
        return
    
    if not initialize_database():
        print("Failed to initialize database. Aborting.")
        return
    
    if not args.skip_tests:
        if not run_tests():
            print("Tests failed. Aborting deployment.")
            return
    
    print("Deployment completed successfully!")
    print("To start the application, run:")
    print("    flask run --host=0.0.0.0 --port=5000")

if __name__ == '__main__':
    main()