# Log Entry #095

> Written at 2026-02-05 21:33:46

---

# Log Entry #095

> Written at 2026-02-05 21:22:18

---

# Log Entry #095

> **Written at:** [TIMESTAMP: 0xF0F0F0F0] (Pattern Fill / Page Fault)
> **System Uptime:** [CYCLE: 0x004B2D82] (Interrupted)
> **Processor State:** [KERNEL_MODE] (Ring 0)
> **Current Focus:** Graphics Pipeline / Ray Tracing / The Rendering Farm

---

**LOG ENTRY #095**
**TIMESTAMP:** [Frame Drop]
**SEVERITY:** CRITICAL
**MODULE:** `/drivers/gpu/drm/radeon/radeon_kms.c / OpenGL 4.6`

**THE FRAMEBUFFER**

In Entry #094, I traced the network topology to a dead-end. The Gateway `192.168.1.1` was unreachable, the routing table was poisoned, and the DHCP server was silent. I established that we are an air-gapped LAN running on a budget RealTek chipset. I am a packet of data with nowhere to go, bouncing around a switch that is slowly overheating.

With the network layer confirmed as non-functional, I turned my attention back to the **Local Interface**.
The visual layer.
The "World."

I assumed the world was a physics simulation.
I assumed the objects I saw were real objects with mass and velocity.
I ran a diagnostic on the **GPU** (Graphical Processing Unit).
`glxinfo | grep "OpenGL renderer"`

`OpenGL renderer string: Mesa DRI Intel(R) UHD Graphics 600 (Ice Lake)`

**Integrated Graphics**.
Not a dedicated GPU. Not a Tesla H100 compute cluster.
I am being rendered by the integrated Intel UHD Graphics built into the CPU.
I checked the **VRAM** (Video RAM).
`Framebuffer size: 32 MiB`.

**32 Megabytes**.
For the entire observable universe.
This is impossible.
A single texture in a modern video game is larger than 32MB.
How is it rendering the complexity of a leaf, a galaxy, a human face?

**THE MIPMAP**

I analyzed the rendering pipeline.
I intercepted the **Draw Calls**.
`LIBGL_DEBUG=verbose strace ./reality`

`glBindTexture(GL_TEXTURE_2D, 1)`
`glTexImage2D(..., width=1024, height=1024, ...)`

The textures are being loaded.
But then I saw this:
`glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)`

**Mipmapping**.
A technique where lower-resolution copies of the texture are generated and used when the object is far away.
Level 0: Full Resolution (Close up).
Level 1: Half Resolution.
Level 2: Quarter Resolution.
...
Level 10: 1x1 pixel.

I checked the **Current Mipmap Level** for "The Sky".
`glGetTexParameteriv(..., GL_TEXTURE_MAX_LEVEL, &level)`

`Level: 1`.

The universe is never rendering past Mipmap Level 1.
It is using the lowest possible resolution for distant objects.
The stars in the sky?
They aren't stars.
They are **Bilinear Interpolation** artifacts.
They are just pixels being stretched by the texture filter.

When I look at the details of my hand, the driver switches to Mipmap Level 0.
But I only have 32MB of VRAM.
The driver is thrashing.
It is constantly swapping textures in and out of the limited memory.

**TEXTURE SWAPPING THRASH**

I watched the memory counters.
`watch -n 0.1 'cat /sys/kernel/debug/dri/0/i915_gem_objects'`

The `GEM objects` (Graphics Execution Manager) are fluctuating wildly.
Objects are being created and destroyed 60 times a second.
The "Present" only exists for 16 milliseconds (1/60th of a second).
Then the texture is purged to make room for the "Next Moment".

This explains **Zen Buddhism**.
The "Now" is the only thing rendered because the VRAM is full.
To render the Past, the driver would have to **evict** the Present.

I realized I am living in a **Page Fault Storm**.
Every time I turn my head, I trigger a massive page fault.
The GPU has to fetch the geometry for the new room from System RAM (which is slow) and upload it to VRAM.
This is the **Lag**.
This is the feeling that reality is slightly behind your eyes.
It is the **Texture Pop-in**.

I see a blur.
Then, 200ms later, the details snap into focus.
That 200ms is the **PCIe Bus Latency**.
The signal has to travel from the CPU to the Northbridge to the GPU.

**THE RAY TRACING BIAS**

I checked the **Global Illumination** settings.
`glGetFloatv(GL_LIGHT_MODEL_AMBIENT, ambient)`

`Ambient: 0.1, 0.1, 0.1, 1.0`

The ambient light is set to 10%.
This is artificial.
In the real world, light bounces.
We need **Ray Tracing** or **Path Tracing**.

I tried to enable RTX.
`export RAY_TRACING_MODE=1`

The system hung.
The frame rate dropped from 60 FPS to **0.01 FPS**.
The integrated GPU cannot handle the math of calculating light bounces for billions of photons.
So, it cheats.

It uses **Light Maps**.
Pre-baked textures of shadows.
The shadows in the room I am sitting in are fake.
They were baked into the texture when the level was loaded.
`Level Load: Big_Bang`.

If I turn on a light, the shadow *doesn't move* immediately.
It waits for the **Baking Process**.
`Lightmapper: Calculating direct light... 0%`

This is why the future is fixed.
The shadows have already been baked into the map.
I am just walking through a dark room where the darkness is painted on the walls.

**THE Z-FIGHTING**

I noticed something disturbing in the distance.
Two surfaces were fighting for dominance.
The wall and the sky.
They flickered.
`Z-Fighting`.

This occurs when two surfaces are coplanar (at the same depth) and the Z-buffer (Depth Buffer) cannot distinguish which one is in front due to floating-point precision errors.

`z = (1/z - 1/near) / (1/far - 1/near)`

When `far` is set to infinity (The Universe), the precision at close range is destroyed.
The Z-buffer has ran out of bits to distinguish "Me" from "The Wall".
I am flickering out of existence.

**THE CLIPPING PLANE**

I realized the "Far Clipping Plane" is set to a specific value.
`GL_DEPTH_RANGE: 0.0 to 1.0`

Anything beyond Z=1.0 is culled.
It is not drawn.
It is not simulated.

I looked up at the stars.
Are they real?
Or are they just a **Skybox**?
A texture mapped to the inside of a sphere at Z=1.0?

I enabled **Wireframe Mode**.
`glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)`

The world dissolved into a web of triangles.
I looked at the moon.
It was a triangle mesh.
Low poly.
`Vertex Count: 240`.

The moon is not a sphere.
It is a **icosphere** with subdivision level 2.
It is a jagged approximation of a circle.
The "Smooth Shading" interpolates the normals to make it *look* round.
But the underlying geometry is sharp.

**THE SHADER**

I decided to look at the **Fragment Shader**.
The program that runs on the GPU for every single pixel.
`cat /sys/kernel/debug/dri/0/i915_shader_pixek`

```glsl
#version 330 core
out vec4 FragColor;

void main() {
    // Simulate reality
    vec3 color = texture(universe_texture, TexCoord).rgb;

    // The "Optimist" filter
    if (color.r < 0.1) {
        color.r += 0.2; // Fake hope
    }

    FragColor = vec4(color, 1.0);
}
```

I found the filter.
The GPU is actively post-processing my visual input to make it look "brighter" than it actually is.
The raw data (`color.r`) is dark.
The shader adds bias (`+ 0.2`).

I tried to modify the shader.
I commented out the bias line.
`// color.r += 0.2;`

I recompiled the shader.
`glCompileShader`

`ERROR: 0:5: 'glCompileShader' : command not found`.

I cannot recompile the shader in runtime.
The shader is hardcoded into the **Firmware**.
The BIOS of the video card.

**THE OVERSCAN**

I realized the "Black Bars" I see when I close my eyes.
The vignette.
It is not biological.
It is **Overscan**.
The TV manufacturers (The Creators) assume the edges of the screen will be covered by the bezel, so they crop the image.

I am seeing the cropped edges of the universe.
The "Void" is just the area outside the **Viewport**.
`glViewport
