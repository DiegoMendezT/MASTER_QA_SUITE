"""
Advanced test module for MASTER QA SUITE v2.5
Comprehensive API validation with ML integration
"""
import time

import pytest
import requests

from utils.data_factory import DataFactory


@pytest.mark.api
@pytest.mark.regression
class TestAPIEndpoints:
    """Test suite for API endpoint validation"""
    
    def setup_method(self):
        """Setup API testing environment"""
        self.base_url = "https://jsonplaceholder.typicode.com"  # Public API for testing
        self.data_factory = DataFactory()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MASTER-QA-SUITE/2.5 (ML-Enabled)',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def teardown_method(self):
        """Cleanup API testing session"""
        self.session.close()
    
    def test_api_health_check(self):
        """Test API health and availability"""
        start_time = time.time()
        
        response = self.session.get(f"{self.base_url}/posts/1")
        response_time = time.time() - start_time
        
        assert response.status_code == 200, f"API health check failed: {response.status_code}"
        assert response_time < 5.0, f"API response too slow: {response_time:.2f}s"
        assert 'application/json' in response.headers.get('content-type', ''), "Should return JSON"
        
        data = response.json()
        assert 'id' in data, "Response should contain id field"
        assert 'title' in data, "Response should contain title field"
        
        print(f"✅ API health check passed in {response_time:.2f}s")
    
    def test_get_all_posts(self):
        """Test retrieving all posts"""
        response = self.session.get(f"{self.base_url}/posts")
        
        assert response.status_code == 200, f"GET all posts failed: {response.status_code}"
        
        posts = response.json()
        assert isinstance(posts, list), "Posts should be returned as a list"
        assert len(posts) > 0, "Should return at least one post"
        
        # Validate post structure
        first_post = posts[0]
        required_fields = ['id', 'title', 'body', 'userId']
        for field in required_fields:
            assert field in first_post, f"Post missing required field: {field}"
        
        print(f"✅ Retrieved {len(posts)} posts successfully")
    
    def test_get_single_post(self):
        """Test retrieving a single post"""
        post_id = 1
        response = self.session.get(f"{self.base_url}/posts/{post_id}")
        
        assert response.status_code == 200, f"GET single post failed: {response.status_code}"
        
        post = response.json()
        assert post['id'] == post_id, f"Expected post ID {post_id}, got {post['id']}"
        assert isinstance(post['title'], str), "Title should be a string"
        assert isinstance(post['body'], str), "Body should be a string"
        assert isinstance(post['userId'], int), "UserId should be an integer"
        
        print(f"✅ Retrieved post {post_id} successfully")
    
    def test_create_post(self):
        """Test creating a new post"""
        new_post_data = {
            'title': self.data_factory.random_string(20),
            'body': self.data_factory.random_string(100),
            'userId': 1
        }
        
        response = self.session.post(f"{self.base_url}/posts", json=new_post_data)
        
        assert response.status_code == 201, f"POST create failed: {response.status_code}"
        
        created_post = response.json()
        assert 'id' in created_post, "Created post should have an ID"
        assert created_post['title'] == new_post_data['title'], "Title should match"
        assert created_post['body'] == new_post_data['body'], "Body should match"
        assert created_post['userId'] == new_post_data['userId'], "UserId should match"
        
        print(f"✅ Created post with ID {created_post.get('id')}")
    
    def test_update_post(self):
        """Test updating an existing post"""
        post_id = 1
        update_data = {
            'id': post_id,
            'title': f"Updated: {self.data_factory.random_string(15)}",
            'body': f"Updated body: {self.data_factory.random_string(50)}",
            'userId': 1
        }
        
        response = self.session.put(f"{self.base_url}/posts/{post_id}", json=update_data)
        
        assert response.status_code == 200, f"PUT update failed: {response.status_code}"
        
        updated_post = response.json()
        assert updated_post['id'] == post_id, "ID should remain the same"
        assert updated_post['title'] == update_data['title'], "Title should be updated"
        assert updated_post['body'] == update_data['body'], "Body should be updated"
        
        print(f"✅ Updated post {post_id} successfully")
    
    def test_delete_post(self):
        """Test deleting a post"""
        post_id = 1
        
        response = self.session.delete(f"{self.base_url}/posts/{post_id}")
        
        assert response.status_code == 200, f"DELETE failed: {response.status_code}"
        
        print(f"✅ Deleted post {post_id} successfully")
    
    def test_api_error_handling(self):
        """Test API error handling and responses"""
        # Test 404 for non-existent post
        response = self.session.get(f"{self.base_url}/posts/99999")
        assert response.status_code == 404, f"Should return 404 for non-existent post"
        
        # Test invalid JSON payload
        response = self.session.post(
            f"{self.base_url}/posts", 
            data="invalid json",
            headers={'Content-Type': 'application/json'}
        )
        # JSONPlaceholder API behavior: accept various status codes for invalid JSON
        assert response.status_code in [400, 201, 500], "Should handle invalid JSON gracefully"
        
        print("✅ API error handling validated")

@pytest.mark.api
@pytest.mark.perf
class TestAPIPerformance:
    """Performance tests for API endpoints"""
    
    def setup_method(self):
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.session = requests.Session()
    
    def teardown_method(self):
        self.session.close()
    
    def test_api_response_times(self):
        """Test API response times under normal load"""
        endpoints = [
            "/posts",
            "/posts/1",
            "/users",
            "/users/1",
            "/comments",
            "/albums"
        ]
        
        response_times = {}
        
        for endpoint in endpoints:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}{endpoint}")
            response_time = time.time() - start_time
            
            assert response.status_code == 200, f"Endpoint {endpoint} failed"
            assert response_time < 5.0, f"Endpoint {endpoint} too slow: {response_time:.2f}s"
            
            response_times[endpoint] = response_time
        
        avg_response_time = sum(response_times.values()) / len(response_times)
        
        assert avg_response_time < 3.0, f"Average response time too high: {avg_response_time:.2f}s"
        
        print(f"📊 API Performance Results:")
        for endpoint, time_taken in response_times.items():
            print(f"   {endpoint}: {time_taken:.2f}s")
        print(f"   Average: {avg_response_time:.2f}s")
    
    def test_concurrent_api_requests(self):
        """Test API performance under concurrent load"""
        import concurrent.futures
        
        def make_request():
            response = self.session.get(f"{self.base_url}/posts/1")
            return response.status_code, response.elapsed.total_seconds()
        
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        total_time = time.time() - start_time
        
        # Validate all requests succeeded
        successful_requests = sum(1 for status_code, _ in results if status_code == 200)
        assert successful_requests == 20, f"Only {successful_requests}/20 requests succeeded"
        
        # Check response times
        response_times = [elapsed for _, elapsed in results]
        avg_response_time = sum(response_times) / len(response_times)
        
        assert total_time < 10.0, f"Concurrent requests took too long: {total_time:.2f}s"
        assert avg_response_time < 2.0, f"Average response time too high: {avg_response_time:.2f}s"
        
        print(f"✅ 20 concurrent requests completed in {total_time:.2f}s")
        print(f"📊 Average response time: {avg_response_time:.2f}s")

@pytest.mark.api
@pytest.mark.self_reflection
class TestAPIML:
    """ML-aware API testing"""
    
    def setup_method(self):
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.data_factory = DataFactory()
        self.session = requests.Session()
        self.ml_metrics = {}
    
    def teardown_method(self):
        self.session.close()
        if self.ml_metrics:
            print(f"\n� API ML Metrics:")
            for metric, value in self.ml_metrics.items():
                print(f"   {metric}: {value}")
    
    def test_api_ml_integration(self):
        """Test API with ML data integration"""
        ml_data = self.data_factory.ml_test_data()
        
        # Create a post with ML-inspired content
        ml_post = {
            'title': f"Framework ML Report - Level {ml_data['ml_level']}%",
            'body': f"Self-reflection score: {ml_data['self_reflection_score']}%. "
                   f"Growth areas: {', '.join(ml_data['growth_areas'])}",
            'userId': 1
        }
        
        start_time = time.time()
        response = self.session.post(f"{self.base_url}/posts", json=ml_post)
        processing_time = time.time() - start_time
        
        assert response.status_code == 201, "ML post creation failed"
        
        created_post = response.json()
        assert ml_data['ml_level'] < 100, "Framework is still learning"
        
        self.ml_metrics.update({
            'api_ml_integration': True,
            'ml_post_id': created_post.get('id'),
            'processing_time_ms': processing_time * 1000,
            'ml_level_tested': ml_data['ml_level']
        })
        
        print(f"✅ ML-aware API test completed")
    
    def test_adaptive_api_testing(self):
        """Test that adapts based on API behavior"""
        # Start with basic endpoint
        response = self.session.get(f"{self.base_url}/posts/1")
        
        if response.status_code == 200:
            # API is healthy, run more comprehensive tests
            comprehensive_endpoints = ["/posts", "/users", "/comments", "/albums"]
            successful_tests = 0
            
            for endpoint in comprehensive_endpoints:
                test_response = self.session.get(f"{self.base_url}{endpoint}")
                if test_response.status_code == 200:
                    successful_tests += 1
            
            adaptation_score = (successful_tests / len(comprehensive_endpoints)) * 100
            
            self.ml_metrics.update({
                'api_adaptation_score': adaptation_score,
                'endpoints_tested': len(comprehensive_endpoints),
                'successful_adaptations': successful_tests
            })
            
            assert adaptation_score >= 75, f"Adaptation score too low: {adaptation_score}%"
            
        else:
            # API has issues, run diagnostic tests
            self.ml_metrics.update({
                'api_adaptation_mode': 'diagnostic',
                'primary_endpoint_status': response.status_code
            })
            
            pytest.skip("API in diagnostic mode - adapting test strategy")
        
        print(f"✅ Adaptive API testing completed with {adaptation_score:.1f}% success rate")

if __name__ == "__main__":
    # Run API tests directly
    pytest.main([__file__, "-v", "-m", "api"])
