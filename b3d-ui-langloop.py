# -*- coding: utf-8 -*-

bl_info = {
    "name": "b3d-ui-langloop",
    "author": "柚桑 / issac",
    "version": (1, 0, 1),
    "blender": (5, 0, 0),
    "location": "Edit > Preferences > Add-ons",
    "description": "快速切換 Blender 介面語系",
    "category": "Interface",
}

import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import IntProperty, EnumProperty
from bpy.app.handlers import persistent


def get_available_languages(self, context):
    """取得所有可用的語系（回調函數版本）"""
    languages = []
    try:
        # 使用 Blender 內建的語系列表和顯示名稱
        import bpy.app.translations as translations
        
        for lang_code in translations.locales:
            # 使用 Blender 的 locale_explode 來取得語言資訊
            try:
                # 嘗試取得該語系的本地化名稱
                lang_name = translations.locale_explode(lang_code)[2]
                if lang_name:
                    display_name = f"{lang_name} - {lang_code}"
                else:
                    display_name = lang_code
            except:
                # 如果無法取得名稱，只顯示代碼
                display_name = lang_code
            
            languages.append((lang_code, display_name, lang_code))
            
    except:
        # 如果無法取得語系列表，返回預設值
        languages = [('en_US', 'English (US) - en_US', 'English (US)')]
    
    if not languages:
        languages = [('en_US', 'English (US) - en_US', 'English (US)')]
    
    return languages


class LANGSWITCH_OT_cycle_language(Operator):
    """循環切換語系"""
    bl_idname = "langswitch.cycle_language"
    bl_label = "b3d-ui-langloop"
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
        
        # 取得當前語系來顯示對應的提示文字
        current_lang = context.preferences.view.language
        
        # 多語言提示文字
        hint_texts = {
            'zh_HANS': "快捷键设置：编辑 > 偏好设定 > 快捷键 > 搜索 'b3d-ui-langloop'",
            'zh_HANT': "快速鍵設定：編輯 > 偏好設定 > 快速鍵 > 搜尋 'b3d-ui-langloop'",
            'ja_JP': "ショートカット設定：編集 > プリファレンス > キーマップ > 'b3d-ui-langloop' を検索",
            'ko_KR': "단축키 설정: 편집 > 환경설정 > 키맵 > 'b3d-ui-langloop' 검색",
            'fr_FR': "Raccourcis clavier : Édition > Préférences > Raccourcis clavier > Rechercher 'b3d-ui-langloop'",
            'de_DE': "Tastenkürzel: Bearbeiten > Einstellungen > Keymap > Suche 'b3d-ui-langloop'",
            'es_ES': "Atajos de teclado: Editar > Preferencias > Keymap > Buscar 'b3d-ui-langloop'",
            'ru_RU': "Горячие клавиши: Правка > Настройки > Сочетания клавиш > Поиск 'b3d-ui-langloop'",
            'it_IT': "Scorciatoie da tastiera: Modifica > Preferenze > Keymap > Cerca 'b3d-ui-langloop'",
            'pt_BR': "Atalhos de teclado: Editar > Preferências > Keymap > Pesquisar 'b3d-ui-langloop'",
            'pt_PT': "Atalhos de teclado: Editar > Preferências > Keymap > Pesquisar 'b3d-ui-langloop'",
            'nl_NL': "Sneltoetsen: Bewerken > Voorkeuren > Keymap > Zoek 'b3d-ui-langloop'",
            'pl_PL': "Skróty klawiszowe: Edycja > Preferencje > Keymap > Szukaj 'b3d-ui-langloop'",
            'tr_TR': "Kısayol tuşları: Düzenle > Tercihler > Keymap > 'b3d-ui-langloop' ara",
            'cs_CZ': "Klávesové zkratky: Upravit > Předvolby > Keymap > Hledat 'b3d-ui-langloop'",
            'ar_EG': "اختصارات لوحة المفاتيح: تحرير > التفضيلات > Keymap > ابحث عن 'b3d-ui-langloop'",
            'th_TH': "ปุ่มลัด: แก้ไข > การตั้งค่า > Keymap > ค้นหา 'b3d-ui-langloop'",
            'vi_VN': "Phím tắt: Chỉnh sửa > Tùy chọn > Keymap > Tìm 'b3d-ui-langloop'",
            'id_ID': "Pintasan keyboard: Edit > Preferensi > Keymap > Cari 'b3d-ui-langloop'",
            'uk_UA': "Гарячі клавіші: Редагування > Налаштування > Keymap > Пошук 'b3d-ui-langloop'",
            'sv_SE': "Kortkommandon: Redigera > Inställningar > Keymap > Sök 'b3d-ui-langloop'",
            'da_DK': "Genveje: Rediger > Indstillinger > Keymap > Søg 'b3d-ui-langloop'",
            'fi_FI': "Pikanäppäimet: Muokkaa > Asetukset > Keymap > Hae 'b3d-ui-langloop'",
            'hu_HU': "Gyorsbillentyűk: Szerkesztés > Beállítások > Keymap > Keresés 'b3d-ui-langloop'",
            'el_GR': "Συντομεύσεις πληκτρολογίου: Επεξεργασία > Προτιμήσεις > Keymap > Αναζήτηση 'b3d-ui-langloop'",
            'ro_RO': "Taste rapide: Editare > Preferințe > Keymap > Căutare 'b3d-ui-langloop'",
            'bg_BG': "Клавишни комбинации: Редактиране > Настройки > Keymap > Търсене 'b3d-ui-langloop'",
            'he_IL': "קיצורי מקלדת: עריכה > העדפות > Keymap > חפש 'b3d-ui-langloop'",
            'hi_IN': "कीबोर्ड शॉर्टकट: संपादित करें > प्राथमिकताएं > Keymap > 'b3d-ui-langloop' खोजें",
            'hr_HR': "Prečaci tipkovnice: Uredi > Postavke > Keymap > Traži 'b3d-ui-langloop'",
            'sk_SK': "Klávesové skratky: Upraviť > Predvoľby > Keymap > Hľadať 'b3d-ui-langloop'",
        }
        
        # 預設英文提示
        hint_text = hint_texts.get(current_lang, 
                                   "Shortcut settings: Edit > Preferences > Keymap > Search 'b3d-ui-langloop'")
        
        layout.label(text=hint_text)
        
        # # 添加恢復快捷鍵按鈕和說明
        # layout.separator()
        # box = layout.box()
        
        # current_lang = context.preferences.view.language
        # info_texts = {
        #     'zh_HANS': "如果快捷键丢失：",
        #     'zh_HANT': "如果快速鍵遺失：",
        #     'ja_JP': "ショートカットが消えた場合：",
        #     'ko_KR': "단축키가 사라진 경우：",
        # }
        # step1_texts = {
        #     'zh_HANS': "1. 点击下方按钮恢复快捷键",
        #     'zh_HANT': "1. 點擊下方按鈕恢復快速鍵",
        #     'ja_JP': "1. 下のボタンをクリック",
        #     'ko_KR': "1. 아래 버튼 클릭",
        # }
        # step2_texts = {
        #     'zh_HANS': "2. 保存偏好设定（Ctrl+Alt+U 或 编辑>偏好设定>保存偏好设定）",
        #     'zh_HANT': "2. 儲存偏好設定（Ctrl+Alt+U 或 編輯>偏好設定>儲存偏好設定）",
        #     'ja_JP': "2. プリファレンスを保存（Ctrl+Alt+U）",
        #     'ko_KR': "2. 환경설정 저장（Ctrl+Alt+U）",
        # }
        # step3_texts = {
        #     'zh_HANS': "3. 重启 Blender",
        #     'zh_HANT': "3. 重啟 Blender",
        #     'ja_JP': "3. Blenderを再起動",
        #     'ko_KR': "3. Blender 재시작",
        # }
        
        # box.label(text=info_texts.get(current_lang, "If keymap is missing:"), icon='INFO')
        # box.label(text=step1_texts.get(current_lang, "1. Click the button below"))
        # box.label(text=step2_texts.get(current_lang, "2. Save Preferences (Ctrl+Alt+U)"))
        # box.label(text=step3_texts.get(current_lang, "3. Restart Blender"))
        
        # row = box.row()
        # row.scale_y = 1.5
        # row.operator("langswitch.restore_keymap", text="🔄 " + ("恢復快捷鍵" if current_lang.startswith('zh') else "Restore Keymap"), icon='FILE_REFRESH')


class LANGSWITCH_OT_restore_keymap(Operator):
    """恢復預設快捷鍵（需要重啟 Blender）"""
    bl_idname = "langswitch.restore_keymap"
    bl_label = "恢復快捷鍵"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        restore_keymap()
        
        # 多語言提示
        current_lang = context.preferences.view.language
        messages = {
            'zh_HANS': "快捷键已恢复！请重启 Blender 以确保生效。",
            'zh_HANT': "快速鍵已恢復！請重啟 Blender 以確保生效。",
            'ja_JP': "ショートカットが復元されました！Blenderを再起動してください。",
            'ko_KR': "단축키가 복원되었습니다! Blender를 재시작하세요.",
        }
        
        msg = messages.get(current_lang, "Keymap restored! Please restart Blender to ensure it takes effect.")
        
        self.report({'WARNING'}, msg)
        return {'FINISHED'}


# 快速鍵映射
addon_keymaps = []


def restore_keymap():
    """恢復快捷鍵的函數"""
    wm = bpy.context.window_manager
    
    # 清除全局列表
    addon_keymaps.clear()
    
    # 嘗試在多個 keyconfig 中恢復
    for kc_type in [wm.keyconfigs.addon, wm.keyconfigs.user]:
        if not kc_type:
            continue
            
        # 找到或創建 Window keymap
        km = None
        for existing_km in kc_type.keymaps:
            if existing_km.name == 'Window' and existing_km.space_type == 'EMPTY':
                km = existing_km
                break
        
        if not km:
            km = kc_type.keymaps.new(name='Window', space_type='EMPTY')
        
        # 移除所有相同 idname 的項目（包括被標記為刪除的）
        items_to_remove = [kmi for kmi in km.keymap_items 
                          if kmi.idname == LANGSWITCH_OT_cycle_language.bl_idname]
        for kmi in items_to_remove:
            try:
                km.keymap_items.remove(kmi)
            except:
                pass
        
        # 重新創建快捷鍵
        try:
            kmi = km.keymap_items.new(
                LANGSWITCH_OT_cycle_language.bl_idname,
                type='T',
                value='PRESS',
                alt=True,
                ctrl=True,
                shift=True
            )
            # 確保是啟用的
            kmi.active = True
            
            # 只將 addon keyconfig 的添加到列表
            if kc_type == wm.keyconfigs.addon:
                addon_keymaps.append((km, kmi))
        except Exception as e:
            print(f"創建快捷鍵時發生錯誤: {e}")
    
    # 強制保存用戶偏好設定以持久化更改
    try:
        bpy.ops.wm.save_userpref()
    except:
        pass


@persistent
def load_post_handler(dummy):
    """在文件加載後檢查並恢復快捷鍵"""
    # 給 Blender 一點時間完全加載
    bpy.app.timers.register(check_and_restore_keymap, first_interval=0.1)


def check_and_restore_keymap():
    """檢查快捷鍵是否存在，不存在則恢復"""
    try:
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.addon
        
        if kc:
            # 檢查是否存在我們的快捷鍵
            has_keymap = False
            for km in kc.keymaps:
                if km.name == 'Window' and km.space_type == 'EMPTY':
                    for kmi in km.keymap_items:
                        if kmi.idname == LANGSWITCH_OT_cycle_language.bl_idname:
                            has_keymap = True
                            break
                    break
            
            # 如果不存在，恢復它
            if not has_keymap:
                restore_keymap()
    except:
        pass
    
    return None  # 不重複執行


def register():
    bpy.utils.register_class(LANGSWITCH_OT_cycle_language)
    bpy.utils.register_class(LANGSWITCH_OT_restore_keymap)
    bpy.utils.register_class(LANGSWITCH_Preferences)
    
    # 註冊快速鍵
    restore_keymap()
    
    # 註冊加載後處理程序
    if load_post_handler not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(load_post_handler)


def unregister():
    # 移除加載後處理程序
    if load_post_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_post_handler)
    
    # 移除快速鍵
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