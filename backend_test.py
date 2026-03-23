import requests
import sys
from datetime import datetime

class ColombiaMapAPITester:
    def __init__(self, base_url="https://narco-impact-map.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.layer_types = ["coca", "violence", "armed_groups", "murders", "poverty"]

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                return True, response.json() if response.content else {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                if response.content:
                    print(f"   Response: {response.text[:200]}...")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timeout")
            return False, {}
        except requests.exceptions.ConnectionError:
            print(f"❌ Failed - Connection error")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test the root API endpoint"""
        success, response = self.run_test(
            "Root API Endpoint",
            "GET",
            "",
            200
        )
        if success and "message" in response:
            print(f"   Message: {response['message']}")
        return success

    def test_layer_endpoints(self):
        """Test all layer endpoints"""
        results = {}
        for layer_type in self.layer_types:
            success, response = self.run_test(
                f"Layer Data - {layer_type}",
                "GET",
                f"layers/{layer_type}",
                200
            )
            results[layer_type] = success
            
            if success:
                # Validate GeoJSON structure
                if "type" in response and response["type"] == "FeatureCollection":
                    features = response.get("features", [])
                    print(f"   ✅ Valid GeoJSON with {len(features)} features")
                    
                    # Check if features have required properties
                    if features:
                        sample_feature = features[0]
                        if "properties" in sample_feature and "geometry" in sample_feature:
                            print(f"   ✅ Features have required properties and geometry")
                        else:
                            print(f"   ⚠️  Features missing properties or geometry")
                else:
                    print(f"   ⚠️  Invalid GeoJSON structure")
            
        return all(results.values())

    def test_stats_endpoints(self):
        """Test statistics endpoints"""
        # Test general stats
        success, response = self.run_test(
            "General Statistics",
            "GET",
            "stats",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   ✅ Received {len(response)} layer statistics")
            
            # Validate stats structure
            for stat in response:
                required_fields = ["layer_name", "total_value", "avg_value", "max_value", "affected_regions"]
                if all(field in stat for field in required_fields):
                    print(f"   ✅ {stat['layer_name']}: {stat['total_value']} total, {stat['affected_regions']} regions")
                else:
                    print(f"   ⚠️  Missing required fields in {stat.get('layer_name', 'unknown')} stats")
        
        # Test individual layer stats
        layer_stats_success = True
        for layer_type in self.layer_types:
            layer_success, layer_response = self.run_test(
                f"Layer Stats - {layer_type}",
                "GET",
                f"stats/{layer_type}",
                200
            )
            if not layer_success:
                layer_stats_success = False
        
        return success and layer_stats_success

    def test_region_endpoints(self):
        """Test region data endpoints"""
        # Test with common Colombian departments
        test_regions = ["Antioquia", "Valle del Cauca", "Nariño", "Putumayo", "Cauca"]
        
        success_count = 0
        for region in test_regions:
            success, response = self.run_test(
                f"Region Data - {region}",
                "GET",
                f"region/{region}",
                200
            )
            
            if success:
                success_count += 1
                if "region" in response and "data" in response:
                    data = response["data"]
                    print(f"   ✅ {region}: {len(data)} data points")
                    
                    # Check if all layer types are present
                    missing_layers = [layer for layer in self.layer_types if layer not in data]
                    if missing_layers:
                        print(f"   ⚠️  Missing data for layers: {missing_layers}")
                else:
                    print(f"   ⚠️  Invalid response structure for {region}")
        
        return success_count > 0

    def test_invalid_endpoints(self):
        """Test error handling for invalid endpoints"""
        # Test invalid layer type
        success, _ = self.run_test(
            "Invalid Layer Type",
            "GET",
            "layers/invalid_layer",
            200  # Should return empty FeatureCollection
        )
        
        # Test invalid region
        success2, _ = self.run_test(
            "Invalid Region",
            "GET",
            "region/NonExistentRegion",
            200  # Should return empty data
        )
        
        return success and success2

def main():
    print("🇨🇴 Colombia Narco Impact Map - API Testing")
    print("=" * 50)
    
    tester = ColombiaMapAPITester()
    
    # Run all tests
    tests = [
        ("Root Endpoint", tester.test_root_endpoint),
        ("Layer Endpoints", tester.test_layer_endpoints),
        ("Statistics Endpoints", tester.test_stats_endpoints),
        ("Region Endpoints", tester.test_region_endpoints),
        ("Error Handling", tester.test_invalid_endpoints)
    ]
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} Tests...")
        try:
            test_func()
        except Exception as e:
            print(f"❌ Test suite {test_name} failed with error: {str(e)}")
    
    # Print final results
    print(f"\n📊 Final Results:")
    print(f"Tests passed: {tester.tests_passed}/{tester.tests_run}")
    success_rate = (tester.tests_passed / tester.tests_run * 100) if tester.tests_run > 0 else 0
    print(f"Success rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("🎉 Backend API tests mostly successful!")
        return 0
    elif success_rate >= 50:
        print("⚠️  Backend API has some issues but basic functionality works")
        return 1
    else:
        print("❌ Backend API has major issues")
        return 2

if __name__ == "__main__":
    sys.exit(main())