from multiprocessing import cpu_count

# ===== GPU DETECTION =====
GPU_BACKEND = None
GPU_DEVICE = None

def detect_gpu():
    """Auto-detect GPU: NVIDIA (CUDA) or CPU fallback."""
    global GPU_BACKEND, GPU_DEVICE
    print("🔍 Detecting GPU capabilities...")

    try:
        import cupy as cp
        if cp.cuda.runtime.getDeviceCount() > 0:
            # TEST PENTING: Cek apakah CuPy bisa benar-benar menjalankan operasi GPU
            # Ini akan memicu error jika CUDA headers/toolkit tidak terinstall di OS
            test_arr = cp.array([1, 2, 3])
            _ = (test_arr * 2).get()
            
            device = cp.cuda.Device(0)
            device_name = device.attributes.get('Name', b'Unknown').decode('utf-8', errors='ignore')
            GPU_BACKEND = 'cuda'
            GPU_DEVICE = device_name
            print(f"  ✓ NVIDIA CUDA detected and working: {device_name}")
            return
    except Exception as e:
        print(f"  ✗ CuPy/CUDA test failed (missing headers/toolkit): {str(e)[:80]}")

    GPU_BACKEND = 'cpu'
    GPU_DEVICE = f"CPU ({cpu_count()} cores)"
    print(f"  ⚙️  Falling back to CPU: {GPU_DEVICE}")