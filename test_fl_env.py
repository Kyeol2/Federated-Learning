"""
Federated Learning Environment Test Script
This script tests if all required packages are installed and working correctly.
"""

import sys

def print_section(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_python_version():
    """Test Python version"""
    print_section("Python Version Check")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("[OK] Python version is compatible")
        return True
    else:
        print("[ERROR] Python 3.7+ required")
        return False

def test_package_import(package_name, display_name=None):
    """Test if a package can be imported"""
    if display_name is None:
        display_name = package_name
    
    try:
        module = __import__(package_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"[OK] {display_name:15s} - version {version}")
        return True
    except ImportError as e:
        print(f"[ERROR] {display_name:15s} - NOT INSTALLED")
        return False

def test_torch_functionality():
    """Test PyTorch basic functionality"""
    print_section("PyTorch Functionality Test")
    
    try:
        import torch
        
        # Create tensors
        x = torch.tensor([1.0, 2.0, 3.0])
        y = torch.tensor([4.0, 5.0, 6.0])
        z = x + y
        
        print(f"Tensor creation: [OK]")
        print(f"  x = {x.numpy()}")
        print(f"  y = {y.numpy()}")
        print(f"  z = x + y = {z.numpy()}")
        
        # Check CUDA availability
        if torch.cuda.is_available():
            print(f"\n[OK] CUDA is available - GPU: {torch.cuda.get_device_name(0)}")
        else:
            print(f"\n[INFO] CUDA not available - using CPU only")
        
        # Create simple neural network
        model = torch.nn.Sequential(
            torch.nn.Linear(10, 20),
            torch.nn.ReLU(),
            torch.nn.Linear(20, 1)
        )
        
        # Test forward pass
        test_input = torch.randn(5, 10)
        output = model(test_input)
        
        print(f"\nNeural Network Test: [OK]")
        print(f"  Input shape: {test_input.shape}")
        print(f"  Output shape: {output.shape}")
        print(f"  Model parameters: {sum(p.numel() for p in model.parameters())}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] PyTorch test failed: {e}")
        return False

def test_numpy_functionality():
    """Test NumPy basic functionality"""
    print_section("NumPy Functionality Test")
    
    try:
        import numpy as np
        
        # Create arrays
        a = np.array([1, 2, 3, 4, 5])
        b = np.array([6, 7, 8, 9, 10])
        c = a + b
        
        print(f"Array creation: [OK]")
        print(f"  a = {a}")
        print(f"  b = {b}")
        print(f"  c = a + b = {c}")
        
        # Matrix operations
        m1 = np.random.randn(3, 3)
        m2 = np.random.randn(3, 3)
        m3 = np.dot(m1, m2)
        
        print(f"\nMatrix operations: [OK]")
        print(f"  Matrix multiplication shape: {m3.shape}")
        print(f"  Mean: {m3.mean():.4f}")
        print(f"  Std: {m3.std():.4f}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] NumPy test failed: {e}")
        return False

def test_simple_federated_learning():
    """Test simple federated learning scenario"""
    print_section("Simple Federated Learning Simulation")
    
    try:
        import torch
        import numpy as np
        
        print("Simulating 3-client federated learning...")
        
        # Global model
        global_model = torch.nn.Linear(5, 1)
        print(f"\n[1] Global model initialized")
        print(f"    Parameters: {sum(p.numel() for p in global_model.parameters())}")
        
        # Simulate 3 clients
        num_clients = 3
        client_models = []
        
        for i in range(num_clients):
            # Each client gets a copy of global model
            client_model = torch.nn.Linear(5, 1)
            client_model.load_state_dict(global_model.state_dict())
            
            # Simulate local training data
            X = torch.randn(10, 5)
            y = torch.randn(10, 1)
            
            # Simple training step
            optimizer = torch.optim.SGD(client_model.parameters(), lr=0.01)
            criterion = torch.nn.MSELoss()
            
            # One epoch
            optimizer.zero_grad()
            output = client_model(X)
            loss = criterion(output, y)
            loss.backward()
            optimizer.step()
            
            client_models.append(client_model)
            print(f"[{i+2}] Client {i+1} trained - Loss: {loss.item():.4f}")
        
        # Aggregate (simple averaging)
        print(f"\n[{num_clients+2}] Aggregating client models...")
        
        with torch.no_grad():
            for param_name, param in global_model.named_parameters():
                avg_param = torch.zeros_like(param)
                for client_model in client_models:
                    client_param = dict(client_model.named_parameters())[param_name]
                    avg_param += client_param
                avg_param /= num_clients
                param.copy_(avg_param)
        
        print(f"[{num_clients+3}] Global model updated successfully!")
        
        # Test global model
        test_input = torch.randn(3, 5)
        test_output = global_model(test_input)
        print(f"\n[TEST] Global model inference:")
        print(f"       Input shape: {test_input.shape}")
        print(f"       Output shape: {test_output.shape}")
        
        print(f"\n[OK] Federated Learning simulation completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] FL simulation failed: {e}")
        return False

def main():
    """Main test function"""
    print("\n" + "="*60)
    print("  Federated Learning Environment Test")
    print("="*60)
    
    results = []
    
    # Test Python version
    results.append(("Python Version", test_python_version()))
    
    # Test package imports
    print_section("Package Installation Check")
    results.append(("PyTorch", test_package_import("torch", "PyTorch")))
    results.append(("NumPy", test_package_import("numpy", "NumPy")))
    results.append(("Pandas", test_package_import("pandas", "Pandas")))
    results.append(("Scikit-learn", test_package_import("sklearn", "Scikit-learn")))
    results.append(("Matplotlib", test_package_import("matplotlib", "Matplotlib")))
    results.append(("Flask", test_package_import("flask", "Flask")))
    results.append(("Requests", test_package_import("requests", "Requests")))
    
    # Test PyTorch functionality
    results.append(("PyTorch Functions", test_torch_functionality()))
    
    # Test NumPy functionality
    results.append(("NumPy Functions", test_numpy_functionality()))
    
    # Test simple FL
    results.append(("FL Simulation", test_simple_federated_learning()))
    
    # Print summary
    print_section("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    print("\nDetailed Results:")
    for test_name, result in results:
        status = "[OK]" if result else "[FAILED]"
        print(f"  {status} {test_name}")
    
    if passed == total:
        print("\n" + "="*60)
        print("  [SUCCESS] All tests passed!")
        print("  Your FL environment is ready to use!")
        print("="*60 + "\n")
        return 0
    else:
        print("\n" + "="*60)
        print(f"  [WARNING] {total - passed} test(s) failed")
        print("  Please check the errors above")
        print("="*60 + "\n")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)