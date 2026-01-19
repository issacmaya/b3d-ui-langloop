# -*- coding: utf-8 -*-

bl_info = {
    "name": "b3d-ui-langloop",
    "author": "Yusang / issac",
    "version": (1, 0, 1),
    "blender": (5, 0, 0),
    "location": "Edit > Preferences > Add-ons",
    "description": "Quick language switching for Blender interface",
    "category": "Interface",
}

import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import IntProperty, EnumProperty
from bpy.app.handlers import persistent


# Internationalization dictionary
i18n_dict = {
    'en_US': {
        'cycle_count': "Cycle Count",
        'cycle_count_desc': "Number of languages to cycle through",
        'language': "Language",
        'select_languages': "Select languages to cycle:",
        'shortcut_hint': "Shortcut settings: Edit > Preferences > Keymap > Search 'b3d-ui-langloop'",
        'restore_keymap': "Restore Keymap",
        'keymap_restored': "Keymap restored! Please restart Blender to ensure it takes effect.",
        'switch_to': "Switched to language:",
    },
    'zh_HANS': {
        'cycle_count': "循环切换数",
        'cycle_count_desc': "要循环切换的语系数量",
        'language': "语系",
        'select_languages': "选择要循环的语系:",
        'shortcut_hint': "快捷键设置:编辑 > 偏好设定 > 快捷键 > 搜索 'b3d-ui-langloop'",
        'restore_keymap': "恢复快捷键",
        'keymap_restored': "快捷键已恢复!请重启 Blender 以确保生效。",
        'switch_to': "切换语系至:",
    },
    'zh_HANT': {
        'cycle_count': "循環切換數",
        'cycle_count_desc': "要循環切換的語系數量",
        'language': "語系",
        'select_languages': "選擇要循環的語系:",
        'shortcut_hint': "快速鍵設定:編輯 > 偏好設定 > 快速鍵 > 搜尋 'b3d-ui-langloop'",
        'restore_keymap': "恢復快速鍵",
        'keymap_restored': "快速鍵已恢復!請重啟 Blender 以確保生效。",
        'switch_to': "切換語系至:",
    },
    'ja_JP': {
        'cycle_count': "循環切替数",
        'cycle_count_desc': "循環切替する言語の数",
        'language': "言語",
        'select_languages': "循環する言語を選択:",
        'shortcut_hint': "ショートカット設定:編集 > プリファレンス > キーマップ > 'b3d-ui-langloop' を検索",
        'restore_keymap': "キーマップを復元",
        'keymap_restored': "キーマップが復元されました!Blenderを再起動してください。",
        'switch_to': "言語を切り替えました:",
    },
    'ko_KR': {
        'cycle_count': "순환 전환 수",
        'cycle_count_desc': "순환 전환할 언어 수",
        'language': "언어",
        'select_languages': "순환할 언어 선택:",
        'shortcut_hint': "단축키 설정: 편집 > 환경설정 > 키맵 > 'b3d-ui-langloop' 검색",
        'restore_keymap': "키맵 복원",
        'keymap_restored': "키맵이 복원되었습니다! Blender를 재시작하세요.",
        'switch_to': "언어 전환:",
    },
    'fr_FR': {
        'cycle_count': "Nombre de cycles",
        'cycle_count_desc': "Nombre de langues à parcourir",
        'language': "Langue",
        'select_languages': "Sélectionnez les langues à parcourir:",
        'shortcut_hint': "Raccourcis clavier: Édition > Préférences > Raccourcis clavier > Rechercher 'b3d-ui-langloop'",
        'restore_keymap': "Restaurer les raccourcis",
        'keymap_restored': "Raccourcis restaurés! Veuillez redémarrer Blender pour assurer la prise en compte.",
        'switch_to': "Langue changée:",
    },
}


def get_text(key, lang=None):
    """Get translated text based on current language"""
    if lang is None:
        try:
            lang = bpy.context.preferences.view.language
        except:
            lang = 'en_US'
    
    # Fallback to English if language not found
    if lang not in i18n_dict:
        lang = 'en_US'
    
    return i18n_dict[lang].get(key, i18n_dict['en_US'].get(key, key))


# Global cache for language list
_cached_languages = []

def build_language_cache():
    """Build language list cache at registration time"""
    global _cached_languages
    _cached_languages = []
    
    # Save current language
    original_lang = bpy.context.preferences.view.language
    
    try:
        # Switch to English to get clean language names
        bpy.context.preferences.view.language = 'en_US'
        
        # Access Blender's language enum
        prefs_view = bpy.types.PreferencesView
        lang_prop = prefs_view.bl_rna.properties['language']
        
        # Build the list
        for item in lang_prop.enum_items:
            _cached_languages.append((item.identifier, item.name, item.identifier))
            
    except Exception as e:
        print(f"Error building language cache: {e}")
        _cached_languages = [('en_US', 'English (US)', 'en_US')]
    finally:
        # Restore original language
        try:
            bpy.context.preferences.view.language = original_lang
        except:
            pass
    
    if not _cached_languages:
        _cached_languages = [('en_US', 'English (US)', 'en_US')]


def get_available_languages(self, context):
    """Get all available languages from cache"""
    global _cached_languages
    
    # If cache is empty, build it now
    if not _cached_languages:
        build_language_cache()
    
    return _cached_languages


class LANGSWITCH_OT_cycle_language(Operator):
    """Cycle through languages"""
    bl_idname = "langswitch.cycle_language"
    bl_label = "b3d-ui-langloop"
    bl_options = {'REGISTER'}

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        current_lang = context.preferences.view.language
        
        # Build the list of configured languages
        lang_list = []
        for i in range(prefs.cycle_count):
            lang_attr = f"language_{i}"
            if hasattr(prefs, lang_attr):
                lang_list.append(getattr(prefs, lang_attr))
        
        # Check if current language is in the list
        try:
            current_index = lang_list.index(current_lang)
            # In list, switch to next
            next_index = (current_index + 1) % prefs.cycle_count
        except ValueError:
            # Not in list, jump to ID 0
            next_index = 0
        
        # Set new language
        if lang_list and next_index < len(lang_list):
            new_lang = lang_list[next_index]
            context.preferences.view.language = new_lang
            self.report({'INFO'}, f"{get_text('switch_to', current_lang)} {new_lang}")
        
        return {'FINISHED'}


class LANGSWITCH_Preferences(AddonPreferences):
    bl_idname = __name__

    def update_cycle_count(self, context):
        """Update when cycle count changes"""
        pass

    cycle_count: IntProperty(
        name="Cycle Count",
        description="Number of languages to cycle through",
        default=2,
        min=2,
        max=10,
        update=update_cycle_count
    )

    # Pre-define 10 language selection fields (using callback function)
    language_0: EnumProperty(
        name="Language 1",
        items=get_available_languages
    )
    
    language_1: EnumProperty(
        name="Language 2",
        items=get_available_languages
    )
    
    language_2: EnumProperty(
        name="Language 3",
        items=get_available_languages
    )
    
    language_3: EnumProperty(
        name="Language 4",
        items=get_available_languages
    )
    
    language_4: EnumProperty(
        name="Language 5",
        items=get_available_languages
    )
    
    language_5: EnumProperty(
        name="Language 6",
        items=get_available_languages
    )
    
    language_6: EnumProperty(
        name="Language 7",
        items=get_available_languages
    )
    
    language_7: EnumProperty(
        name="Language 8",
        items=get_available_languages
    )
    
    language_8: EnumProperty(
        name="Language 9",
        items=get_available_languages
    )
    
    language_9: EnumProperty(
        name="Language 10",
        items=get_available_languages
    )

    def draw(self, context):
        layout = self.layout
        current_lang = context.preferences.view.language
        
        # Cycle count setting
        layout.prop(self, "cycle_count", text=get_text('cycle_count', current_lang))
        
        layout.separator()
        layout.label(text=get_text('select_languages', current_lang))
        
        # Display language selection fields based on cycle_count
        box = layout.box()
        for i in range(self.cycle_count):
            box.prop(self, f"language_{i}", text=f"{get_text('language', current_lang)} {i+1}")
        
        layout.separator()
        layout.label(text=get_text('shortcut_hint', current_lang))


class LANGSWITCH_OT_restore_keymap(Operator):
    """Restore default keymap (requires Blender restart)"""
    bl_idname = "langswitch.restore_keymap"
    bl_label = "Restore Keymap"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        restore_keymap()
        current_lang = context.preferences.view.language
        self.report({'WARNING'}, get_text('keymap_restored', current_lang))
        return {'FINISHED'}


# Keymap storage
addon_keymaps = []


def restore_keymap():
    """Function to restore keymap"""
    wm = bpy.context.window_manager
    
    # Clear global list
    addon_keymaps.clear()
    
    # Try to restore in multiple keyconfigs
    for kc_type in [wm.keyconfigs.addon, wm.keyconfigs.user]:
        if not kc_type:
            continue
            
        # Find or create Window keymap
        km = None
        for existing_km in kc_type.keymaps:
            if existing_km.name == 'Window' and existing_km.space_type == 'EMPTY':
                km = existing_km
                break
        
        if not km:
            km = kc_type.keymaps.new(name='Window', space_type='EMPTY')
        
        # Remove all items with the same idname (including those marked for deletion)
        items_to_remove = [kmi for kmi in km.keymap_items 
                          if kmi.idname == LANGSWITCH_OT_cycle_language.bl_idname]
        for kmi in items_to_remove:
            try:
                km.keymap_items.remove(kmi)
            except:
                pass
        
        # Recreate keymap
        try:
            kmi = km.keymap_items.new(
                LANGSWITCH_OT_cycle_language.bl_idname,
                type='L',
                value='PRESS',
                ctrl=True,
                shift=True
            )
            # Ensure it's enabled
            kmi.active = True
            
            # Only add addon keyconfig to list
            if kc_type == wm.keyconfigs.addon:
                addon_keymaps.append((km, kmi))
        except Exception as e:
            print(f"Error creating keymap: {e}")
    
    # Force save user preferences to persist changes
    try:
        bpy.ops.wm.save_userpref()
    except:
        pass


@persistent
def load_post_handler(dummy):
    """Check and restore keymap after file load"""
    # Give Blender some time to fully load
    bpy.app.timers.register(check_and_restore_keymap, first_interval=0.1)


def check_and_restore_keymap():
    """Check if keymap exists, restore if not"""
    try:
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.addon
        
        if kc:
            # Check if our keymap exists
            has_keymap = False
            for km in kc.keymaps:
                if km.name == 'Window' and km.space_type == 'EMPTY':
                    for kmi in km.keymap_items:
                        if kmi.idname == LANGSWITCH_OT_cycle_language.bl_idname:
                            has_keymap = True
                            break
                    break
            
            # If it doesn't exist, restore it
            if not has_keymap:
                restore_keymap()
    except:
        pass
    
    return None  # Don't repeat execution


def register():
    bpy.utils.register_class(LANGSWITCH_OT_cycle_language)
    bpy.utils.register_class(LANGSWITCH_OT_restore_keymap)
    bpy.utils.register_class(LANGSWITCH_Preferences)
    
    # Build language cache at registration time
    build_language_cache()
    
    # Register keymap
    restore_keymap()
    
    # Register load post handler
    if load_post_handler not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(load_post_handler)


def unregister():
    # Remove load post handler
    if load_post_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_post_handler)
    
    # Remove keymap
    for km, kmi in addon_keymaps:
        try:
            km.keymap_items.remove(kmi)
        except:
            pass
    
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(LANGSWITCH_Preferences)
    bpy.utils.unregister_class(LANGSWITCH_OT_restore_keymap)
    bpy.utils.unregister_class(LANGSWITCH_OT_cycle_language)


if __name__ == "__main__":
    register()