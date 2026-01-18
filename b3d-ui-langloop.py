# -*- coding: utf-8 -*-

bl_info = {
    "name": "b3d-ui-langloop",
    "author": "柚桑 / issac",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "Edit > Preferences > Add-ons",
    "description": "快速切換 Blender 介面語系",
    "category": "Interface",
}

import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import IntProperty, EnumProperty


def get_available_languages(self, context):
    """取得所有可用的語系（回調函數版本）"""
    languages = []
    try:
        for lang in bpy.app.translations.locales:
            languages.append((lang, lang, lang))
    except:
        # 如果無法取得語系列表，返回預設值
        languages = [('en_US', 'English', 'English')]
    
    if not languages:
        languages = [('en_US', 'English', 'English')]
    
    return languages


class LANGSWITCH_OT_cycle_language(Operator):
    """循環切換語系"""
    bl_idname = "langswitch.cycle_language"
    bl_label = "Cycle Language"
    bl_options = {'REGISTER'}

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        current_lang = context.preferences.view.language
        
        # 建立已設定的語系列表
        lang_list = []
        for i in range(prefs.cycle_count):
            lang_attr = f"language_{i}"
            if hasattr(prefs, lang_attr):
                lang_list.append(getattr(prefs, lang_attr))
        
        # 檢查當前語系是否在列表中
        try:
            current_index = lang_list.index(current_lang)
            # 在列表中，切換到下一個
            next_index = (current_index + 1) % prefs.cycle_count
        except ValueError:
            # 不在列表中，跳到 ID 0
            next_index = 0
        
        # 設定新語系
        if lang_list and next_index < len(lang_list):
            context.preferences.view.language = lang_list[next_index]
            self.report({'INFO'}, f"切換語系至: {lang_list[next_index]}")
        
        return {'FINISHED'}


class LANGSWITCH_Preferences(AddonPreferences):
    bl_idname = __name__

    def update_cycle_count(self, context):
        """當循環切換數改變時更新"""
        pass

    cycle_count: IntProperty(
        name="循環切換數",
        description="要循環切換的語系數量",
        default=2,
        min=2,
        max=10,
        update=update_cycle_count
    )

    # 預先定義 10 個語系選擇欄位（使用回調函數）
    language_0: EnumProperty(
        name="語系 1",
        items=get_available_languages
    )
    
    language_1: EnumProperty(
        name="語系 2",
        items=get_available_languages
    )
    
    language_2: EnumProperty(
        name="語系 3",
        items=get_available_languages
    )
    
    language_3: EnumProperty(
        name="語系 4",
        items=get_available_languages
    )
    
    language_4: EnumProperty(
        name="語系 5",
        items=get_available_languages
    )
    
    language_5: EnumProperty(
        name="語系 6",
        items=get_available_languages
    )
    
    language_6: EnumProperty(
        name="語系 7",
        items=get_available_languages
    )
    
    language_7: EnumProperty(
        name="語系 8",
        items=get_available_languages
    )
    
    language_8: EnumProperty(
        name="語系 9",
        items=get_available_languages
    )
    
    language_9: EnumProperty(
        name="語系 10",
        items=get_available_languages
    )

    def draw(self, context):
        layout = self.layout
        
        # 循環切換數設定
        layout.prop(self, "cycle_count")
        
        layout.separator()
        layout.label(text="選擇要循環的語系：")
        
        # 根據 cycle_count 顯示對應數量的語系選擇欄位
        box = layout.box()
        for i in range(self.cycle_count):
            box.prop(self, f"language_{i}")
        
        layout.separator()
        layout.label(text="快速鍵設定請至：編輯 > 偏好設定 > 快速鍵 > 搜尋 'Cycle Language'")


# 快速鍵映射
addon_keymaps = []


def register():
    bpy.utils.register_class(LANGSWITCH_OT_cycle_language)
    bpy.utils.register_class(LANGSWITCH_Preferences)
    
    # 註冊快速鍵
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Window', space_type='EMPTY')
        kmi = km.keymap_items.new(
            LANGSWITCH_OT_cycle_language.bl_idname,
            type='L',
            value='PRESS',
            ctrl=True,
            shift=True
        )
        addon_keymaps.append((km, kmi))


def unregister():
    # 移除快速鍵
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(LANGSWITCH_Preferences)
    bpy.utils.unregister_class(LANGSWITCH_OT_cycle_language)


if __name__ == "__main__":
    register()