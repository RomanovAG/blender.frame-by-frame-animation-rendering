bl_info = {
    "name": "Render Frames One by One",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (3, 6, 4),
    "location": "Properties > Render > Render One by One",
    "description": "Renders animation frames sequentially and saves them to a specified path.",
    "category": "Render",
}

import bpy
import os

class RenderOneByOneProperties(bpy.types.PropertyGroup):
    output_path: bpy.props.StringProperty(
        name="Output Path",
        subtype='DIR_PATH',
        default="//",
        description="Define the output path for the rendered frames"
    )

class OBJECT_OT_RenderOneByOne(bpy.types.Operator):
    bl_idname = "render.render_one_by_one"
    bl_label = "Render One by One"
    bl_description = "Render frames one by one automatically"
    
    @classmethod
    def poll(cls, context):
        return context.scene.render_one_by_one_props.output_path != ""
    
    def execute(self, context):
        scene = context.scene
        start_frame = scene.frame_start
        end_frame = scene.frame_end
        output_path = bpy.path.abspath(scene.render_one_by_one_props.output_path)

        # Ensure the directory exists before rendering
        if not os.path.exists(output_path):
            self.report({'ERROR'}, "Output path does not exist.")
            return {'CANCELLED'}

        for frame in range(start_frame, end_frame + 1):
            scene.frame_set(frame)
            scene.render.filepath = os.path.join(output_path, f"frame_{frame:03d}")
            bpy.ops.render.render(write_still=True)
        
        return {'FINISHED'}

class RENDER_PT_RenderOneByOne(bpy.types.Panel):
    bl_label = "Render One by One"
    bl_idname = "RENDER_PT_render_one_by_one"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    
    def draw(self, context):
        layout = self.layout
        render_one_by_one_props = context.scene.render_one_by_one_props
        
        layout.prop(render_one_by_one_props, "output_path")
        layout.operator(OBJECT_OT_RenderOneByOne.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_RenderOneByOne)
    bpy.utils.register_class(RenderOneByOneProperties)
    bpy.utils.register_class(RENDER_PT_RenderOneByOne)
    bpy.types.Scene.render_one_by_one_props = bpy.props.PointerProperty(type=RenderOneByOneProperties)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_RenderOneByOne)
    bpy.utils.unregister_class(RenderOneByOneProperties)
    bpy.utils.unregister_class(RENDER_PT_RenderOneByOne)
    del bpy.types.Scene.render_one_by_one_props

if __name__ == "__main__":
    register()
