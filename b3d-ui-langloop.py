# -*- coding: utf-8 -*-

bl_info = {
    "name": "b3d-ui-langloop",
    "author": "柚桑 / issac",
    "version": (1, 0, 0),
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
        'switch_to': "Switched to language:",
        'current_shortcut': "Current shortcut: {key}",
        'shortcut_missing': "Missing (please refer to manual)",
    },
    'en_GB': {
        'cycle_count': "Cycle Count",
        'cycle_count_desc': "Number of languages to cycle through",
        'language': "Language",
        'select_languages': "Select languages to cycle:",
        'shortcut_hint': "Shortcut settings: Edit > Preferences > Keymap > Search 'b3d-ui-langloop'",
        'switch_to': "Switched to language:",
        'current_shortcut': "Current shortcut: {key}",
        'shortcut_missing': "Missing (please refer to manual)",
    },
    'zh_HANS': {
        'cycle_count': "循环切换数",
        'cycle_count_desc': "要循环切换的语系数量",
        'language': "语系",
        'select_languages': "选择要循环的语系:",
        'shortcut_hint': "快捷键设置: 编辑 > 偏好设定 > 快捷键 > 搜索 'b3d-ui-langloop'",
        'switch_to': "切换语系至:",
        'current_shortcut': "当前快捷键: {key}",
        'shortcut_missing': "遗失 (请查阅使用手册)",
    },
    'zh_HANT': {
        'cycle_count': "循環切換數",
        'cycle_count_desc': "要循環切換的語系數量",
        'language': "語系",
        'select_languages': "選擇要循環的語系:",
        'shortcut_hint': "快速鍵設定: 編輯 > 偏好設定 > 快速鍵 > 搜尋 'b3d-ui-langloop'",
        'switch_to': "切換語系至:",
        'current_shortcut': "目前快速鍵: {key}",
        'shortcut_missing': "遺失 (請查閱使用手冊)",
    },
    'ja_JP': {
        'cycle_count': "循環切替数",
        'cycle_count_desc': "循環切替する言語の数",
        'language': "言語",
        'select_languages': "循環する言語を選択:",
        'shortcut_hint': "ショートカット設定: 編集 > プリファレンス > キーマップ > 'b3d-ui-langloop' を検索",
        'switch_to': "言語を切り替えました:",
        'current_shortcut': "現在のショートカット: {key}",
        'shortcut_missing': "見つかりません (マニュアルを参照)",
    },
    'ko_KR': {
        'cycle_count': "순환 전환 수",
        'cycle_count_desc': "순환 전환할 언어 수",
        'language': "언어",
        'select_languages': "순환할 언어 선택:",
        'shortcut_hint': "단축키 설정: 편집 > 환경설정 > 키맵 > 'b3d-ui-langloop' 검색",
        'switch_to': "언어 전환:",
        'current_shortcut': "현재 단축키: {key}",
        'shortcut_missing': "누락됨 (사용 설명서 참조)",
    },
    'fr_FR': {
        'cycle_count': "Nombre de cycles",
        'cycle_count_desc': "Nombre de langues à parcourir",
        'language': "Langue",
        'select_languages': "Sélectionnez les langues à parcourir:",
        'shortcut_hint': "Raccourcis clavier: Édition > Préférences > Raccourcis clavier > Rechercher 'b3d-ui-langloop'",
        'switch_to': "Langue changée:",
        'current_shortcut': "Raccourci actuel: {key}",
        'shortcut_missing': "Manquant (veuillez consulter le manuel)",
    },
    'de_DE': {
        'cycle_count': "Anzahl der Zyklen",
        'cycle_count_desc': "Anzahl der Sprachen zum Durchlaufen",
        'language': "Sprache",
        'select_languages': "Wählen Sie Sprachen zum Durchlaufen:",
        'shortcut_hint': "Tastenkombinationen: Bearbeiten > Einstellungen > Tastenbelegung > 'b3d-ui-langloop' suchen",
        'switch_to': "Sprache gewechselt zu:",
        'current_shortcut': "Aktuelle Tastenkombination: {key}",
        'shortcut_missing': "Fehlt (bitte Handbuch konsultieren)",
    },
    'es': {
        'cycle_count': "Número de ciclos",
        'cycle_count_desc': "Número de idiomas para recorrer",
        'language': "Idioma",
        'select_languages': "Seleccione idiomas para recorrer:",
        'shortcut_hint': "Configuración de atajos: Editar > Preferencias > Atajos de teclado > Buscar 'b3d-ui-langloop'",
        'switch_to': "Idioma cambiado a:",
        'current_shortcut': "Atajo actual: {key}",
        'shortcut_missing': "Falta (consulte el manual)",
    },
    'it_IT': {
        'cycle_count': "Numero di cicli",
        'cycle_count_desc': "Numero di lingue da scorrere",
        'language': "Lingua",
        'select_languages': "Seleziona le lingue da scorrere:",
        'shortcut_hint': "Impostazioni scorciatoie: Modifica > Preferenze > Scorciatoie > Cerca 'b3d-ui-langloop'",
        'switch_to': "Lingua cambiata in:",
        'current_shortcut': "Scorciatoia attuale: {key}",
        'shortcut_missing': "Mancante (consultare il manuale)",
    },
    'pt_PT': {
        'cycle_count': "Número de ciclos",
        'cycle_count_desc': "Número de idiomas para percorrer",
        'language': "Idioma",
        'select_languages': "Selecione idiomas para percorrer:",
        'shortcut_hint': "Configurações de atalhos: Editar > Preferências > Atalhos > Pesquisar 'b3d-ui-langloop'",
        'switch_to': "Idioma alterado para:",
        'current_shortcut': "Atalho atual: {key}",
        'shortcut_missing': "Em falta (consulte o manual)",
    },
    'pt_BR': {
        'cycle_count': "Número de ciclos",
        'cycle_count_desc': "Número de idiomas para percorrer",
        'language': "Idioma",
        'select_languages': "Selecione idiomas para percorrer:",
        'shortcut_hint': "Configurações de atalhos: Editar > Preferências > Atalhos > Pesquisar 'b3d-ui-langloop'",
        'switch_to': "Idioma alterado para:",
        'current_shortcut': "Atalho atual: {key}",
        'shortcut_missing': "Ausente (consulte o manual)",
    },
    'ru_RU': {
        'cycle_count': "Количество циклов",
        'cycle_count_desc': "Количество языков для переключения",
        'language': "Язык",
        'select_languages': "Выберите языки для переключения:",
        'shortcut_hint': "Настройки горячих клавиш: Правка > Настройки > Горячие клавиши > Найти 'b3d-ui-langloop'",
        'switch_to': "Язык изменен на:",
        'current_shortcut': "Текущая горячая клавиша: {key}",
        'shortcut_missing': "Отсутствует (см. руководство)",
    },
    'pl_PL': {
        'cycle_count': "Liczba cykli",
        'cycle_count_desc': "Liczba języków do przełączania",
        'language': "Język",
        'select_languages': "Wybierz języki do przełączania:",
        'shortcut_hint': "Ustawienia skrótów: Edycja > Preferencje > Skróty klawiszowe > Szukaj 'b3d-ui-langloop'",
        'switch_to': "Język zmieniony na:",
        'current_shortcut': "Bieżący skrót: {key}",
        'shortcut_missing': "Brak (zobacz instrukcję)",
    },
    'nl_NL': {
        'cycle_count': "Aantal cycli",
        'cycle_count_desc': "Aantal talen om door te bladeren",
        'language': "Taal",
        'select_languages': "Selecteer talen om door te bladeren:",
        'shortcut_hint': "Sneltoets instellingen: Bewerken > Voorkeuren > Sneltoetsen > Zoek 'b3d-ui-langloop'",
        'switch_to': "Taal gewijzigd naar:",
        'current_shortcut': "Huidige sneltoets: {key}",
        'shortcut_missing': "Ontbreekt (raadpleeg handleiding)",
    },
    'sv_SE': {
        'cycle_count': "Antal cykler",
        'cycle_count_desc': "Antal språk att växla mellan",
        'language': "Språk",
        'select_languages': "Välj språk att växla mellan:",
        'shortcut_hint': "Genvägar: Redigera > Inställningar > Tangentbindningar > Sök 'b3d-ui-langloop'",
        'switch_to': "Språk bytt till:",
        'current_shortcut': "Nuvarande genväg: {key}",
        'shortcut_missing': "Saknas (se manual)",
    },
    'cs_CZ': {
        'cycle_count': "Počet cyklů",
        'cycle_count_desc': "Počet jazyků k procházení",
        'language': "Jazyk",
        'select_languages': "Vyberte jazyky k procházení:",
        'shortcut_hint': "Nastavení klávesových zkratek: Upravit > Předvolby > Klávesové zkratky > Hledat 'b3d-ui-langloop'",
        'switch_to': "Jazyk změněn na:",
        'current_shortcut': "Aktuální zkratka: {key}",
        'shortcut_missing': "Chybí (viz manuál)",
    },
    'tr_TR': {
        'cycle_count': "Döngü sayısı",
        'cycle_count_desc': "Geçiş yapılacak dil sayısı",
        'language': "Dil",
        'select_languages': "Geçiş yapılacak dilleri seçin:",
        'shortcut_hint': "Kısayol ayarları: Düzenle > Tercihler > Tuş atamaları > 'b3d-ui-langloop' ara",
        'switch_to': "Dil değiştirildi:",
        'current_shortcut': "Mevcut kısayol: {key}",
        'shortcut_missing': "Eksik (kılavuza bakın)",
    },
    'ar_EG': {
        'cycle_count': "عدد الدورات",
        'cycle_count_desc': "عدد اللغات للتبديل بينها",
        'language': "اللغة",
        'select_languages': "اختر اللغات للتبديل بينها:",
        'shortcut_hint': "إعدادات الاختصارات: تحرير > التفضيلات > اختصارات لوحة المفاتيح > ابحث عن 'b3d-ui-langloop'",
        'switch_to': "تم تغيير اللغة إلى:",
        'current_shortcut': "الاختصار الحالي: {key}",
        'shortcut_missing': "مفقود (يرجى الرجوع إلى الدليل)",
    },
    'he_IL': {
        'cycle_count': "מספר מחזורים",
        'cycle_count_desc': "מספר השפות למעבר ביניהן",
        'language': "שפה",
        'select_languages': "בחר שפות למעבר ביניהן:",
        'shortcut_hint': "הגדרות קיצורי דרך: עריכה > העדפות > מקשי קיצור > חפש 'b3d-ui-langloop'",
        'switch_to': "שפה שונתה ל:",
        'current_shortcut': "קיצור דרך נוכחי: {key}",
        'shortcut_missing': "חסר (עיין במדריך)",
    },
    'th_TH': {
        'cycle_count': "จำนวนรอบ",
        'cycle_count_desc': "จำนวนภาษาที่จะสลับ",
        'language': "ภาษา",
        'select_languages': "เลือกภาษาที่จะสลับ:",
        'shortcut_hint': "การตั้งค่าทางลัด: แก้ไข > การตั้งค่า > แป้นพิมพ์ลัด > ค้นหา 'b3d-ui-langloop'",
        'switch_to': "เปลี่ยนภาษาเป็น:",
        'current_shortcut': "ทางลัดปัจจุบัน: {key}",
        'shortcut_missing': "หายไป (โปรดดูคู่มือ)",
    },
    'uk_UA': {
        'cycle_count': "Кількість циклів",
        'cycle_count_desc': "Кількість мов для перемикання",
        'language': "Мова",
        'select_languages': "Виберіть мови для перемикання:",
        'shortcut_hint': "Налаштування гарячих клавіш: Правка > Налаштування > Гарячі клавіші > Знайти 'b3d-ui-langloop'",
        'switch_to': "Мову змінено на:",
        'current_shortcut': "Поточна гаряча клавіша: {key}",
        'shortcut_missing': "Відсутня (див. посібник)",
    },
    'vi_VN': {
        'cycle_count': "Số chu kỳ",
        'cycle_count_desc': "Số ngôn ngữ để chuyển đổi",
        'language': "Ngôn ngữ",
        'select_languages': "Chọn ngôn ngữ để chuyển đổi:",
        'shortcut_hint': "Cài đặt phím tắt: Chỉnh sửa > Tùy chọn > Phím tắt > Tìm kiếm 'b3d-ui-langloop'",
        'switch_to': "Đã chuyển ngôn ngữ sang:",
        'current_shortcut': "Phím tắt hiện tại: {key}",
        'shortcut_missing': "Thiếu (vui lòng xem hướng dẫn)",
    },
    'id_ID': {
        'cycle_count': "Jumlah siklus",
        'cycle_count_desc': "Jumlah bahasa untuk berpindah",
        'language': "Bahasa",
        'select_languages': "Pilih bahasa untuk berpindah:",
        'shortcut_hint': "Pengaturan pintasan: Edit > Preferensi > Pemetaan Kunci > Cari 'b3d-ui-langloop'",
        'switch_to': "Bahasa diubah ke:",
        'current_shortcut': "Pintasan saat ini: {key}",
        'shortcut_missing': "Hilang (silakan lihat manual)",
    },
    'hi_IN': {
        'cycle_count': "चक्र की संख्या",
        'cycle_count_desc': "स्विच करने के लिए भाषाओं की संख्या",
        'language': "भाषा",
        'select_languages': "स्विच करने के लिए भाषाएँ चुनें:",
        'shortcut_hint': "शॉर्टकट सेटिंग्स: संपादित करें > प्राथमिकताएं > कीमैप > 'b3d-ui-langloop' खोजें",
        'switch_to': "भाषा बदली गई:",
        'current_shortcut': "वर्तमान शॉर्टकट: {key}",
        'shortcut_missing': "गायब (कृपया मैनुअल देखें)",
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


def get_current_keymap_string():
    """Get current keymap as a human-readable string, or missing message"""
    try:
        wm = bpy.context.window_manager
        
        # Check in multiple keyconfigs (user has priority over addon)
        for kc in [wm.keyconfigs.user, wm.keyconfigs.addon]:
            if not kc:
                continue
                
            # Search for our keymap item
            for km in kc.keymaps:
                if km.name == 'Window' and km.space_type == 'EMPTY':
                    for kmi in km.keymap_items:
                        if kmi.idname == LANGSWITCH_OT_cycle_language.bl_idname and kmi.active:
                            # Found it! Build the key string
                            key_parts = []
                            if kmi.ctrl:
                                key_parts.append("Ctrl")
                            if kmi.alt:
                                key_parts.append("Alt")
                            if kmi.shift:
                                key_parts.append("Shift")
                            if kmi.oskey:
                                key_parts.append("Cmd")
                            
                            # Add the main key
                            key_parts.append(kmi.type)
                            
                            return "+".join(key_parts)
        
        # Not found
        return None
        
    except Exception as e:
        print(f"Error getting keymap: {e}")
        return None


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


class LANGSWITCH_OT_add_language(Operator):
    """Add a language slot"""
    bl_idname = "langswitch.add_language"
    bl_label = "Add Language"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        if prefs.cycle_count < 10:
            prefs.cycle_count += 1
        return {'FINISHED'}


class LANGSWITCH_OT_remove_language(Operator):
    """Remove a language slot"""
    bl_idname = "langswitch.remove_language"
    bl_label = "Remove Language"
    bl_options = {'REGISTER', 'UNDO'}
    
    index: IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        if prefs.cycle_count > 2 and self.index >= 2:
            # Shift languages down to fill the gap
            for i in range(self.index, prefs.cycle_count - 1):
                lang_attr_current = f"language_{i}"
                lang_attr_next = f"language_{i + 1}"
                setattr(prefs, lang_attr_current, getattr(prefs, lang_attr_next))
            
            # Decrease count
            prefs.cycle_count -= 1
        return {'FINISHED'}


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
        
        layout.separator()
        layout.label(text=get_text('select_languages', current_lang))
        
        # Display language selection fields with remove buttons
        box = layout.box()
        for i in range(self.cycle_count):
            row = box.row(align=True)
            
            # Remove button column
            btn_col = row.column(align=True)
            if i < 2:
                # Disable for first two languages
                btn_col.enabled = False
            remove_op = btn_col.operator("langswitch.remove_language", text="", icon='REMOVE')
            remove_op.index = i
            
            # Language selection dropdown
            row.prop(self, f"language_{i}", text=f"{get_text('language', current_lang)} {i+1}")
        
        # Add button (only show if less than 10 languages)
        if self.cycle_count < 10:
            row = box.row()
            row.operator("langswitch.add_language", text="", icon='ADD')
        
        layout.separator()
        layout.label(text=get_text('shortcut_hint', current_lang))
        
        # Display current keymap status
        layout.separator()
        keymap_str = get_current_keymap_string()
        if keymap_str:
            # Keymap found - display it
            status_text = get_text('current_shortcut', current_lang).format(key=keymap_str)
            layout.label(text=status_text, icon='KEYINGSET')
        else:
            # Keymap missing
            layout.label(text=get_text('shortcut_missing', current_lang), icon='ERROR')


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
                type='T',
                value='PRESS',
                ctrl=True,
                alt=True,
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
    bpy.utils.register_class(LANGSWITCH_OT_add_language)
    bpy.utils.register_class(LANGSWITCH_OT_remove_language)
    bpy.utils.register_class(LANGSWITCH_OT_cycle_language)
    bpy.utils.register_class(LANGSWITCH_Preferences)
    
    # Build language cache at registration time
    build_language_cache()
    
    # Register keymap - simple version
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Window', space_type='EMPTY')
        kmi = km.keymap_items.new(
            LANGSWITCH_OT_cycle_language.bl_idname,
            type='T',
            value='PRESS',
            ctrl=True,
            alt=True,
            shift=True
        )
        addon_keymaps.append((km, kmi))


def unregister():
    # Remove keymap - simple version
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(LANGSWITCH_Preferences)
    bpy.utils.unregister_class(LANGSWITCH_OT_cycle_language)
    bpy.utils.unregister_class(LANGSWITCH_OT_remove_language)
    bpy.utils.unregister_class(LANGSWITCH_OT_add_language)


if __name__ == "__main__":
    register()