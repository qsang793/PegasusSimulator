# Migration Guide: Pegasus Simulator to Isaac Sim 5.0

This document outlines the necessary changes to migrate Pegasus Simulator from Isaac Sim 4.5.0 to Isaac Sim 5.0.

## Summary of Changes

### 1. Extension Dependencies (extension.toml)

**Updated:**

- `version = "5.0.0"` (from 4.5.0)
- `"omni.isaac.core" = {}` → `"isaacsim.core.api" = {}`
- `"omni.kit.window.viewport" = {}` → `"omni.kit.viewport.utility" = {}`

**Added:**

- `"isaacsim.core.prims" = {}`
- `"isaacsim.core.utils" = {}`
- `"omni.isaac.dynamic_control" = {}` (deprecated but still needed)
- `"isaacsim.sensors.camera" = {}`

### 2. Core API Changes

#### A. Dynamic Control Interface (CRITICAL UPDATE)

**Status:** Using deprecated but working interface

**Important Note:** The `omni.isaac.dynamic_control` extension is deprecated in Isaac Sim 5.0 but still functional. We're keeping it for compatibility until a full migration to the new Core API can be completed.

**Current Approach:**
```python
# CURRENT (Working in Isaac Sim 5.0)
from omni.isaac.dynamic_control import _dynamic_control
self._vehicle_dc_interface = _dynamic_control.acquire_dynamic_control_interface()
```

**Files Using This:**
- `pegasus/simulator/logic/vehicles/multirotor.py`
- `pegasus/simulator/logic/vehicles/vehicle.py`

#### B. Sensor APIs

**Deprecated:** `omni.isaac.sensor`
**Replacement:** `isaacsim.sensors.camera`

**Files Updated:**
- `pegasus/simulator/logic/graphs/ros2_camera_graph.py`
- `pegasus/simulator/logic/graphical_sensors/monocular_camera.py`

**Changes Made:**
```python
# OLD
from omni.isaac.sensor import Camera

# NEW
from isaacsim.sensors.camera import Camera
```

### 3. Complete Dependencies for extension.toml

```toml
[dependencies]
"omni.ui" = {}
"omni.usd" = {}
"omni.kit.uiapp" = {}
"isaacsim.core.api" = {}
"isaacsim.core.prims" = {}
"isaacsim.core.utils" = {}
"omni.ui.scene" = {}
"omni.kit.viewport.utility" = {}
"isaacsim.replicator.agent.core" = {}
"omni.isaac.dynamic_control" = {}
"isaacsim.sensors.camera" = {}
```

## Testing Strategy

1. **Extension Load Test:** Try loading the extension in Isaac Sim 5.0
2. **Single Vehicle Test:** Test spawning a single drone
3. **PX4 Integration Test:** Verify MAVLink communication still works
4. **Multi-vehicle Test:** Test multiple drones
5. **Sensor Test:** Verify all sensors (IMU, GPS, Camera) work correctly

## Current Status

- [x] Extension configuration updated
- [x] Dynamic control imports maintained (using deprecated but working interface)
- [x] Sensor imports updated
- [x] Version numbers updated
- [x] All required dependencies added
- [ ] Full testing in Isaac Sim 5.0 environment needed

## Known Issues & Resolutions

### Issue 1: Dynamic Control Deprecation Warning
**Problem:** `omni.isaac.dynamic_control` shows deprecation warnings
**Resolution:** This is expected. The extension still works in Isaac Sim 5.0 but will be removed in future versions.

### Issue 2: Future Migration Path
**Problem:** Eventually need to migrate away from dynamic control
**Solution:** Future update should migrate to the new `isaacsim.core.api` physics interface, but this requires significant code changes to all the physics interaction methods.

## Future Migration Path (Not Implemented Yet)

For a complete migration away from deprecated APIs, these changes would be needed:

1. **Replace Dynamic Control with Core API:**
   ```python
   # FUTURE MIGRATION (Not implemented)
   from isaacsim.core.api.robots import Articulation
   from isaacsim.core.api.prims import RigidPrim
   ```

2. **Update Physics Methods:**
   - Replace `get_articulation()` with new Core API methods
   - Replace `apply_body_force()` with new physics methods
   - Replace `set_dof_velocity()` with new joint control methods

## Immediate Next Steps

1. **Test Extension Loading**
   ```bash
   # Try loading the extension in Isaac Sim 5.0
   # Check for any remaining import errors
   ```

2. **Verify Core Functionality**
   - Test vehicle spawning
   - Test PX4 MAVLink connection
   - Test sensor data flow

3. **Address Deprecation Warnings**
   - Document which features use deprecated APIs
   - Plan future migration timeline

## Additional Resources

- [Isaac Sim 5.0 Migration Guide](https://docs.isaacsim.omniverse.nvidia.com/latest/overview/extensions_renaming.html)
- [Isaac Sim 5.0 Release Notes](https://docs.isaacsim.omniverse.nvidia.com/latest/overview/release_notes.html)
- [New Core API Documentation](https://docs.isaacsim.omniverse.nvidia.com/5.0.0/py/source/extensions/isaacsim.core.api/docs/index.html)
