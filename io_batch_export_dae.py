import bpy
import os

bl_info = {
 "name": "DAE Batch Exporter",
 "description": "Bath export objects to individual DAE files.",
 "author": "Happenstance",
 "blender": (2, 7, 5),
 "version": (0, 1, 0),
 "category": "Exporter",
 "location": "",
 "warning": "",
 "wiki_url": "",
 "tracker_url": "",
}

class DAEBatchExportPane(bpy.types.Panel):
    bl_idname = "dae_batch_exporter_id"
    bl_label = "DAE Batch Exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.label(text="Batch Export:")
        col.prop(context.scene, 'dae_batch_export_path')
        row = col.row(align=True)
        row.operator("dae.batch_exporter", text="Batch Export", icon='EXPORT')


class DAEBatchExporter(bpy.types.Operator):
    bl_idname = "dae.batch_exporter"
    bl_label = "Choose Directory"

    def execute(self, context):
        print ("DAEBatchExporter.execute()")

        basedir = os.path.dirname(bpy.data.filepath)
        if not basedir:
            raise Exception("Save .blend file before exporting!")

        if context.scene.dae_batch_export_path == "":
            raise Exception("Missing export path! Choose a directory before continuing.")

        # select all visible meshes
        mesh=[]
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='MESH')
        col = bpy.context.selected_objects

        # convert path to windows friendly notation
        dir = os.path.dirname(bpy.path.abspath(context.scene.dae_batch_export_path))
        # cursor to origin
        bpy.context.scene.cursor_location = (0.0, 0.0, 0.0)

        # iterate through all objects, select each individually, and export (using mesh name as file name)
        for obj in col:
            # select only current object
            bpy.ops.object.select_all(action='DESELECT')
            obj.select = True
            
            # freeze location, rotation and scale
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            
            # set pivot point to cursor location
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            
            # store mesh
            mesh.append(obj)
            
            # use mesh name for file name
            name = bpy.path.clean_name(obj.name)
            fn = os.path.join(dir, name)
            print("exporting: " + fn)
            
            # export to dae
            bpy.ops.wm.collada_export(filepath=fn + ".dae", selected=True)

        return {'FINISHED'}

# registers
def register():
    bpy.types.Scene.dae_batch_export_path = bpy.props.StringProperty (
        name="Export Path",
        default="",
        description="Location of exported files.",
        subtype='DIR_PATH'
    )
    bpy.utils.register_class(DAEBatchExportPane)
    bpy.utils.register_class(DAEBatchExporter)


def unregister():
    del bpy.types.Scene.dae_batch_export_path
    bpy.utils.unregister_class(DAEBatchExportPane)
    bpy.utils.unregister_class(DAEBatchExporter)

if __name__ == "__main__":
    register()