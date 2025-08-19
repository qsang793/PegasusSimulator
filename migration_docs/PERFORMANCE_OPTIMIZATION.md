# Pegasus Simulator Performance Optimization Guide

This guide helps resolve common performance issues and warning messages in Isaac Sim 5.0.

## Recent Fixes Applied

### ✅ **Camera Warning Fixes**

**Issue:** Repeated camera aperture and deprecated API warnings causing lag
```
[Warning] [isaacsim.sensors.camera.camera] 'verticalAperture' and 'horizontalAperture' are inconsistent
[Warning] [isaacsim.sensors.camera.camera] Camera.get_projection_type is deprecated
```

**Solutions Applied:**
1. **Fixed deprecated API usage**: Replaced `get_projection_type()` with `get_lens_distortion_model()`
2. **Fixed aperture consistency**: Automatically calculate vertical aperture based on resolution aspect ratio
3. **Reduced update frequency**: Default camera frequency reduced from 60Hz to 10Hz
4. **Added update throttling**: Camera data only updates every 5th call
5. **Better error handling**: Prevents repeated error logging

### ✅ **GPU Memory Optimization**

**Issue:** `Client gpu.foundation.plugin has acquired interface 100 times`

**Solution:** Dynamic control interface is now cached and reused instead of repeatedly acquired.

## Performance Configuration Options

### 1. Camera Performance Settings

For minimal performance impact, use these camera settings:

```python
from pegasus.simulator.logic.graphical_sensors.monocular_camera import MonocularCamera

# Low performance impact camera config
camera_config = {
    "frequency": 5,           # Very low frequency (5 Hz)
    "resolution": (640, 480), # Lower resolution
    "depth": False,           # Disable depth if not needed
}

camera = MonocularCamera("camera", config=camera_config)
```

### 2. Vehicle Backend Settings

For better performance, disable unnecessary features:

```python
backend_config = {
    "px4_autolaunch": False,  # Manual PX4 launch for better control
    "update_rate": 100.0,     # Reduced from 250 Hz
    "enable_lockstep": False, # Disable if real-time sync not critical
}
```

### 3. World Settings Optimization

```python
# In your simulation setup
world_settings = {
    "physics_dt": 1.0 / 100.0,    # Reduced physics rate
    "rendering_dt": 1.0 / 30.0,   # Reduced rendering rate
    "device": "cpu",              # Use GPU if available
}
```

## Isaac Sim General Performance Tips

### 1. **Reduce Viewport Rendering**
- Close unnecessary viewport windows
- Reduce viewport resolution in Settings → Viewport

### 2. **Disable Unnecessary Extensions**
- Window → Extensions → Disable unused extensions
- Especially heavy ones like LiveSync, Flow, etc.

### 3. **Physics Optimization**
- Use simpler collision meshes
- Reduce contact points for vehicles
- Use GPU physics if available

### 4. **Scene Optimization**
- Use simpler environments for testing
- Avoid complex materials with many textures
- Use LOD (Level of Detail) models when available

## Monitoring Performance

### Check Current Frame Rate:
- Window → Viewport → Show Performance Info
- Monitor FPS and simulation rate

### Memory Usage:
- Window → Performance Profiler
- Monitor GPU and RAM usage

### Debug Logging:
```python
# Reduce log verbosity
import carb
carb.settings.get_settings().set("/log/level", carb.log.LEVEL_WARN)
```

## Quick Performance Checklist

- [ ] Camera frequency ≤ 10 Hz
- [ ] Physics rate ≤ 100 Hz  
- [ ] Rendering rate ≤ 60 Hz
- [ ] Use simple environments for testing
- [ ] Disable depth cameras if not needed
- [ ] Close extra viewport windows
- [ ] Monitor system resources (CPU/GPU/RAM)

## Troubleshooting Common Issues

### Issue: High CPU Usage
**Solution:** Reduce physics and camera update rates

### Issue: High GPU Memory Usage  
**Solution:** Lower camera resolution, disable depth, use simpler materials

### Issue: Simulation Running Slow
**Solution:** Check real-time factor in timeline, reduce scene complexity

### Issue: Warning Messages in Loop
**Solution:** Check this guide for specific warning fixes applied

## Reporting Performance Issues

When reporting performance issues, include:
1. Isaac Sim version
2. GPU model and memory
3. CPU specs and core count  
4. Scene complexity (number of vehicles, camera resolution)
5. Specific warning messages
6. FPS and real-time factor values

## Latest Updates

**August 15, 2025:**
- Fixed camera aperture warnings
- Fixed deprecated API warnings  
- Reduced default camera update rates
- Added camera update throttling
- Improved error handling in camera updates
