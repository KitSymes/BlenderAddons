bl_info = {
    "name": "Clone Vertex Groups Order",
    "description": "Clone the order of vertex groups between objects, names must match.",
    "author": "Kit Symes",
    "version": (1, 0),
    "blender": (2, 91, 0),
    "category": "Rigging",
}
import bpy
from bpy import context

m_list = []

class CopyOrder(bpy.types.Operator):
    """Copy the order of Vertex Groups"""
    bl_idname = "object.copy_vertex_groups_order"
    bl_label = "Copy Vertex Groups Order"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global m_list
        
        obj = context.active_object
        v_groups = obj.vertex_groups
        m_list = []
        
        for n in v_groups:
            m_list.append(n.name)

        return {'FINISHED'}

class PasteOrder(bpy.types.Operator):
    """Paste the order of Vertex Groups"""
    bl_idname = "object.paste_vertex_groups_order"
    bl_label = "Paste Vertex Groups Order"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global m_list
        
        obj = context.active_object
        v_groups = obj.vertex_groups
        offset = 0
        
        for i in range(len(m_list)):
            if m_list[i] in v_groups:
                v_groups.active_index = v_groups.find(m_list[i])
                vgmove(v_groups.find(m_list[i]) - i + offset)
            else:
                offset += 1

        return {'FINISHED'}

def vgmove(delta): # Taken from https://blender.stackexchange.com/questions/137444/how-can-i-move-reorder-a-vertex-group-more-than-one-spot-at-a-time
    direction = 'UP' if delta > 0 else 'DOWN'
    for i in range(abs(delta)):
        bpy.ops.object.vertex_group_move(direction=direction)

def menu_func(self, context):
    self.layout.operator(CopyOrder.bl_idname)
    self.layout.operator(PasteOrder.bl_idname)

def register():
    bpy.utils.register_class(CopyOrder)
    bpy.utils.register_class(PasteOrder)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(PasteOrder)
    bpy.utils.unregister_class(CopyOrder)