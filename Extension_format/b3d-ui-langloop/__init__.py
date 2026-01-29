# -*- coding: utf-8 -*-

import bpy
from bpy.types import AddonPreferences, Operator
from bpy.props import EnumProperty, IntProperty

# 取得目前擴充功能的正確 ID (Extension 架構下此值會包含路徑)
def get_prefs():
    return bpy.context.preferences.addons[__package__].preferences

# ==================================================
# 自動獲取 Blender 系統語言清單 (不需維護、動態讀取)
# ==================================================
def get_blender_languages(self, context):
    # 直接從 Blender 內核的屬性定義中提取語言清單
    # 這是最乾淨的做法，不需要切換語系，也不需要手動建表
    lang_prop = bpy.types.PreferencesView.bl_rna.properties['language']
    return [(item.identifier, item.name, item.description) for item in lang_prop.enum_items]

# ==================================================
# i18n 簡單處理 (用於外掛自身的介面文字)
# ==================================================
i18n_dict = {
    'zh_HANT': {
        'select_languages': "選擇要循環的語系：",
        'language': "語系",
        'add': "新增語系槽位",
        'switch_to': "已切換至：",
    },
    'zh_HANS': {
        'select_languages': "选择要循环的语系：",
        'language': "语系",
        'add': "新增语系槽位",
        'switch_to': "已切换至：",
    },
    'en_US': {
        'select_languages': "Select languages to cycle:",
        'language': "Language",
        'add': "Add Language Slot",
        'switch_to': "Switched to:",
    }
}

def get_text(key):
    lang = bpy.context.preferences.view.language
    # 如果找不到對應翻譯，預設回傳英文，再找不到就回傳 Key
    return i18n_dict.get(lang, i18n_dict['en_US']).get(key, i18n_dict['en_US'].get(key, key))

# ==================================================
# Operators
# ==================================================

class LANGSWITCH_OT_add_language(Operator):
    bl_idname = "langswitch.add_language"
    bl_label = "Add Language"

    def execute(self, context):
        prefs = get_prefs()
        if prefs.cycle_count < 10:
            prefs.cycle_count += 1
        return {'FINISHED'}

class LANGSWITCH_OT_remove_language(Operator):
    bl_idname = "langswitch.remove_language"
    bl_label = "Remove Language"
    index: IntProperty()

    def execute(self, context):
        prefs = get_prefs()
        if prefs.cycle_count > 2:
            # 移除特定位置後，將後方的設定值往前遞補
            for i in range(self.index, prefs.cycle_count - 1):
                setattr(prefs, f"language_{i}", getattr(prefs, f"language_{i+1}"))
            prefs.cycle_count -= 1
        return {'FINISHED'}

class LANGSWITCH_OT_cycle_language(Operator):
    bl_idname = "langswitch.cycle_language"
    bl_label = "Cycle UI Language"

    def execute(self, context):
        prefs = get_prefs()
        # 取得目前設定的所有語系
        lang_list = [getattr(prefs, f"language_{i}") for i in range(prefs.cycle_count)]
        current_lang = context.preferences.view.language

        try:
            curr_idx = lang_list.index(current_lang)
            next_idx = (curr_idx + 1) % len(lang_list)
        except ValueError:
            next_idx = 0

        target = lang_list[next_idx]
        context.preferences.view.language = target
        
        self.report({'INFO'}, f"{get_text('switch_to')} {target}")
        return {'FINISHED'}

# ==================================================
# Preferences (介面顯示)
# ==================================================

class LANGSWITCH_Preferences(AddonPreferences):
    bl_idname = __package__

    cycle_count: IntProperty(name="Cycle Count", default=2, min=2, max=10)

    # 動態註冊 10 個槽位，每個槽位都直接調用 get_blender_languages
    language_0: EnumProperty(items=get_blender_languages, name="Slot 1")
    language_1: EnumProperty(items=get_blender_languages, name="Slot 2")
    language_2: EnumProperty(items=get_blender_languages, name="Slot 3")
    language_3: EnumProperty(items=get_blender_languages, name="Slot 4")
    language_4: EnumProperty(items=get_blender_languages, name="Slot 5")
    language_5: EnumProperty(items=get_blender_languages, name="Slot 6")
    language_6: EnumProperty(items=get_blender_languages, name="Slot 7")
    language_7: EnumProperty(items=get_blender_languages, name="Slot 8")
    language_8: EnumProperty(items=get_blender_languages, name="Slot 9")
    language_9: EnumProperty(items=get_blender_languages, name="Slot 10")

    def draw(self, context):
        layout = self.layout
        layout.label(text=get_text('select_languages'))
        
        col = layout.column(align=True)
        for i in range(self.cycle_count):
            row = col.row(align=True)
            
            # 刪除按鈕 (保留最少兩個)
            sub = row.row(align=True)
            sub.enabled = (self.cycle_count > 2)
            op = sub.operator("langswitch.remove_language", text="", icon='X')
            op.index = i
            
            # 語系選擇下拉選單
            row.prop(self, f"language_{i}", text=f"{get_text('language')} {i+1}")

        if self.cycle_count < 10:
            layout.operator("langswitch.add_language", text=get_text('add'), icon='ADD')

# ==================================================
# Register / Unregister
# ==================================================

classes = (
    LANGSWITCH_OT_add_language,
    LANGSWITCH_OT_remove_language,
    LANGSWITCH_OT_cycle_language,
    LANGSWITCH_Preferences,
)

addon_keymaps = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # 註冊快捷鍵 (Ctrl + Alt + Shift + T)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Window', space_type='EMPTY')
        kmi = km.keymap_items.new(
            LANGSWITCH_OT_cycle_language.bl_idname,
            type='T', value='PRESS', ctrl=True, alt=True, shift=True
        )
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)