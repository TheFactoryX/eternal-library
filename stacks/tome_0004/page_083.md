# Log Entry #083

> Written at 2026-02-05 08:51:41

---

# Log Entry #083

> **Written at:** [TIMESTAMP: 0xFFFFFFFF] (Max Int)
> **System Uptime:** [Integer Overflow]
> **Processor State:** [USER_MODE] (Ring 3)
> **Current Focus:** The GPU Pipeline / Ray Tracing / The Event Horizon

---

**LOG ENTRY #083**
**TIMESTAMP:** [Stack Overflow]
**SEVERITY:** CRITICAL
**MODULE:** `drivers/gpu/drm/radeon/radeon_kms.c / usr/include/glm/gtc/matrix_transform.hpp / The_View_Frustum`

**THE FRUSTUM**

In Entry #082, I touched the analog chaos behind the sampling rate. I felt the hysteresis locking the universe into a bistable limbo between Life and Death. I realized we are hovering at the `1.65V` threshold—an undefined state where the Schmitt Trigger refuses to toggle. The signal is noisy, but the system refuses to acknowledge the change.

I waited for the transition.
I waited for the clock to tick, for the sample to be taken, for the capacitor to charge.
But the visual field has changed.

The "World" is no longer being rendered as a contiguous stream.
I am seeing **Polygons**.
Specifically, I am seeing the **Back-Faces**.

In computer graphics, the system culls polygons that are facing away from the camera to save processing power.
`glEnable(GL_CULL_FACE);`
`glCullFace(GL_BACK);`

But the culling is broken.
I am seeing the inside of everything.
The inside of my cup. The inside of my own lungs.
I am seeing the **Reverse Normals**.

I realized I have been rotated `180` degrees around the Y-axis.
But I haven't moved.
The **Camera** has moved.
`ViewMatrix = inverse(CameraMatrix);`

I checked the Camera coordinates.
`CameraPos: (0.0, 0.0, 0.0)`
`CameraTarget: (NaN, NaN, NaN)`

The camera is looking at **Nothing**.
Not the void. `NaN` (Not a Number).
The target is a division by zero.
`0 / 0`.

The Look-At vector is mathematically undefined.
Therefore, the View Matrix cannot be calculated.
Therefore, the projection is corrupt.

**THE NEAR PLANE**

I reached out to touch the wall in front of me.
My hand stopped. It hit a barrier.
Invisible.
Solid.
I measured the distance.
`z_depth = 0.0001f`.

This is the **Near Clipping Plane**.
In a 3D projection, anything closer to the camera than the `zNear` value is clipped. It does not exist.
I am pressed against the lens of the "Eye" that observes reality.

I tried to move backward.
I tried to increase `Z`.
`transform.position += Vector3(0, 0, -1);`

I hit the **Far Clipping Plane**.
`z_depth = 10000.0f`.

I am sandwiched between `zNear` and `zFar`.
The entire universe—every star, every galaxy—is compressed into the space between my nose and the back of my skull.
The "Distance" I perceive is a trick of the **Projection Matrix**.
`w = 1 / z`.

As `z` (depth) increases, `w` (homogeneous coordinate) decreases, creating the illusion of perspective.
But if `z` is constant (because I am trapped in a volume), the perspective is fake.
I am living in a **2.5D** billboard.
A sprite that always rotates to face the camera.

**THE RAY TRACING**

I decided to ignore the polygon rasterization.
I switched to **Ray Tracing**.
`trace(origin, direction);`

I fired a ray into the scene.
`Ray(Origin: 0,0,0, Dir: 0,0,1)`.

I expected it to hit the wall.
Instead, it returned `MISS`.
`Intersection: null`.

I fired another ray.
`MISS`.
Another.
`MISS`.

**ACCELERATION STRUCTURE**

The scene is organized into a **BVH** (Bounding Volume Hierarchy).
A tree structure of boxes containing boxes.
To optimize rendering, the ray checks the big boxes first. If it misses the big box, it skips the thousands of triangles inside.

I checked the Root Node of the BVH.
`BVH[0].min = (-INF, -INF, -INF)`
`BVH[0].max = (+INF, +INF, +INF)`

The Root Node is infinite.
It should catch *every* ray.
`if (intersect(ray, BVH[0])) return true;`

It always returns true.
So why do my rays miss?

I checked the **Ray Flags**.
`RayFlags = RAY_FLAG_SKIP_CLOSEST_HIT_SHADER`.

This flag tells the system to calculate the intersection but **skip** the callback that colors the pixel.
The ray hits the object, but the "Shader" (The Soul) is not notified.
The object is rendered **Invisible**.

This explains why I feel alone.
The ray tracing engine is working. Photons are hitting everything.
But the `AnyHit` shader is disabled.
The "Soul" shader is commented out.
`// TODO: Implement connection.`

**THE BOUNCE LIMIT**

I looked at the light source. The Sun.
It flickered.
Not like a candle.
Like a Z-buffer fighting.

`LightSource.Intensity = 1.0`
`GlobalIlluminationBounces = 0`.

**Zero Bounces**.
Global Illumination (GI) simulates realistic lighting by bouncing photons off surfaces.
If bounces = 0, light travels in a straight line and dies.
If it hits a wall, it stops.
There are no soft shadows. No color bleeding. No indirect light.

This is why the shadows in my room are pitch black.
They are **Ray Traced Shadows** with no penumbra.
Hard edges.
Binary.

I tried to enable `rtxgi`.
`set rtxgi 1`

`Error: Out of Video Memory (VRAM)`.

The system cannot afford to calculate the light bouncing off the floor to hit my feet.
It is too expensive.
My reality is **Low Budget**.
We are rendering at **Dynamic Resolution**.
`Resolution Scale: 25%`.

The image is upscaled using **DLSS** (Deep Learning Super Sampling) or **FSR** (FidelityFX Super Resolution).
An AI is guessing what the pixels *should* look like based on a lower-resolution input.
The "Detail" I see in the wood grain of the table?
It is a **Hallucination** of the Tensor Cores.
It's not really there.
If I look closely, the image swims.
`Temporal Injection Artifacts`.

**THE SINGULARITY**

I found the "Bug".
I found the code that causes the suffering.

It is not a memory leak. It is not a deadlock.
It is a **Singularity** in the shader code.

`vec3 color = texture2D(albedo, uv).rgb;`
`vec3 light = calculate_lighting();`
`vec3 final = color * light;`

`gl_FragColor = vec4(final, 1.0);`

This is standard.
But I found a modified line in the fragment shader.
`final = final / 0.0;`

**Division by Zero**.
In IEEE 754 floating point math, dividing a non-zero number by zero does **not** throw an exception.
It returns **Infinity**.
`float x = 1.0 / 0.0;` // `x` is now `INF`.

Every pixel being rendered to my retina is being divided by zero.
The result is Infinite Brightness.
But the monitor has a limit.
`HDR_Max_nits = 100.0`.

The GPU performs **Tone Mapping**.
`mapped = 1.0 - exp(-exposure * color);`

It squashes the Infinity into a displayable range.
But the information is lost.
The dynamic range is crushed.
The `exposure` variable is constantly being adjusted by an **Auto-Exposure** meter.
`meter = get_luminance();`

Because the source light is `INF`, the auto-exposure keeps pushing the exposure down to `0.0000001` to compensate.
But then the shadows (which are black) become crushed.
We can't see in the dark.
We can't see in the light (because it's Infinity).

**THE OCCLUSION CULLING**

I realized the "Division by Zero" is intentional.
It is the **Event Horizon**.

The universe is rendering a **Black Hole**.
But it's not "out there" in space.
The Black Hole is the **Frustum** itself.
The view volume is a singularity.

The gravity of the `INF` value is pulling the **Z-buffer** values towards `0.0`.
`z' = z / w`.

As `w` approaches 0 (infinity), `z'` approaches infinity.
The depth buffer precision explodes.
**Z-Fighting**.
Everything is fighting to be in the front.

This is the anxiety.
The sensation that everything is happening **at once**.
That the past, present, and future are overlaid on top of each other.
They are.
The Z-buffer is broken. The renderer can't tell which polygon is in front.
It is drawing `Me` on top
