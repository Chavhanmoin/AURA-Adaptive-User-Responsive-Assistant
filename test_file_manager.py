from file_manager import *
import os

def test_file_manager():
    """Test all file manager functions"""
    
    print("🗂️ TESTING FILE MANAGER FUNCTIONS")
    print("=" * 50)
    
    # Test paths
    test_folder = "C:\\temp\\jarvis_test"
    test_file = "C:\\temp\\jarvis_test\\test.txt"
    
    print("1. Testing create_folder()")
    result = create_folder(test_folder)
    print(f"Result: {result}")
    
    print("\n2. Testing create_file()")
    result = create_file(test_file, "Hello from JARVIS!")
    print(f"Result: {result}")
    
    print("\n3. Testing list_files()")
    result = list_files(test_folder)
    print(f"Result: {result}")
    
    print("\n4. Testing open_folder()")
    result = open_folder(test_folder)
    print(f"Result: {result}")
    
    print("\n5. Testing copy_file()")
    copy_dest = "C:\\temp\\jarvis_test\\test_copy.txt"
    result = copy_file(test_file, copy_dest)
    print(f"Result: {result}")
    
    print("\n6. Testing move_file()")
    move_dest = "C:\\temp\\jarvis_test\\test_moved.txt"
    result = move_file(copy_dest, move_dest)
    print(f"Result: {result}")
    
    print("\n7. Testing delete_file()")
    result = delete_file(move_dest)
    print(f"Result: {result}")
    
    print("\n8. Testing delete_folder()")
    result = delete_folder(test_folder)
    print(f"Result: {result}")
    
    print("\n" + "=" * 50)
    print("✅ File Manager Tests Completed")

if __name__ == "__main__":
    test_file_manager()