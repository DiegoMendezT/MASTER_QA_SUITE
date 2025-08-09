"""
Test data factory for MASTER QA SUITE v2.0
Generate randomized test data for various test scenarios
"""
import random
import string
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

class DataFactory:
    """Factory class for generating test data"""
    
    @staticmethod
    def random_string(length=10):
        """Generate random string of specified length"""
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    @staticmethod
    def random_email():
        """Generate random email address"""
        username = DataFactory.random_string(8).lower()
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'test.com']
        domain = random.choice(domains)
        return f"{username}@{domain}"
    
    @staticmethod
    def random_phone():
        """Generate random phone number"""
        return f"+1{random.randint(1000000000, 9999999999)}"
    
    @staticmethod
    def random_name():
        """Generate random full name"""
        return fake.name()
    
    @staticmethod
    def random_address():
        """Generate random address"""
        return {
            'street': fake.street_address(),
            'city': fake.city(),
            'state': fake.state(),
            'zip_code': fake.zipcode(),
            'country': fake.country()
        }
    
    @staticmethod
    def random_date(start_date=None, end_date=None):
        """Generate random date between start and end dates"""
        if not start_date:
            start_date = datetime.now() - timedelta(days=365)
        if not end_date:
            end_date = datetime.now()
        
        return fake.date_between(start_date=start_date, end_date=end_date)
    
    @staticmethod
    def random_user_data():
        """Generate complete random user data"""
        return {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': DataFactory.random_email(),
            'phone': DataFactory.random_phone(),
            'username': DataFactory.random_string(12).lower(),
            'password': DataFactory.random_password(),
            'address': DataFactory.random_address(),
            'birth_date': DataFactory.random_date(
                start_date=datetime(1950, 1, 1),
                end_date=datetime(2005, 1, 1)
            )
        }
    
    @staticmethod
    def random_password(length=12, include_symbols=True):
        """Generate random password"""
        characters = string.ascii_letters + string.digits
        if include_symbols:
            characters += "!@#$%^&*"
        
        password = ''.join(random.choices(characters, k=length))
        return password
    
    @staticmethod
    def random_search_terms():
        """Generate random search terms for testing"""
        terms = [
            "Python automation", "Selenium WebDriver", "JavaScript testing",
            "QA best practices", "Test automation", "Continuous integration",
            "API testing", "Mobile testing", "Performance testing",
            "Security testing", "Load testing", "Unit testing"
        ]
        return random.choice(terms)
    
    @staticmethod
    def random_url():
        """Generate random URL"""
        return fake.url()
    
    @staticmethod
    def random_company():
        """Generate random company data"""
        return {
            'name': fake.company(),
            'email': fake.company_email(),
            'phone': DataFactory.random_phone(),
            'website': fake.url(),
            'industry': random.choice([
                'Technology', 'Healthcare', 'Finance', 'Education', 
                'Retail', 'Manufacturing', 'Consulting'
            ])
        }
    
    @staticmethod
    def consciousness_test_data():
        """Generate data specifically for framework self-reflection tests"""
        return {
            'framework_name': 'MASTER_QA_SUITE',
            'version': '2.5',
            'birth_date': '2025-08-07',
            'consciousness_level': round(random.uniform(20.0, 95.0), 1),
            'self_reflection_score': random.randint(80, 100),
            'mastery_metrics': {
                'tests_passed': random.randint(10, 100),
                'execution_time': round(random.uniform(1.0, 60.0), 2),
                'success_rate': round(random.uniform(85.0, 100.0), 2),
                'coverage_score': round(random.uniform(70.0, 100.0), 1)
            },
            'growth_areas': [
                'selenium_automation',
                'self_reflection', 
                'consciousness_logging',
                'best_practices',
                'client_readiness'
            ]
        }
    
    @staticmethod
    def invalid_login_scenarios():
        """Generate various invalid login scenarios for negative testing"""
        return [
            {'username': '', 'password': ''},  # Empty credentials
            {'username': fake.user_name(), 'password': ''},  # Missing password
            {'username': '', 'password': DataFactory.random_password()},  # Missing username
            {'username': 'admin', 'password': 'password123'},  # Common weak combo
            {'username': fake.user_name(), 'password': '123'},  # Too short password
            {'username': 'invalid-email', 'password': fake.password()},  # Invalid email
            {'username': fake.user_name() * 5, 'password': fake.password()},  # Too long
        ]
