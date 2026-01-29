# -*- coding: utf-8 -*-

import bpy
from bpy.types import AddonPreferences, Operator
from bpy.props import EnumProperty, IntProperty

# ==================================================
# 核心修正：使用與原版一致的 Cache 機制與路徑獲取
# ==================================================

# 在新版 Extension 架構中，這能確保 Preferences 讀寫正確
def get_prefs():
    return bpy.context.preferences.addons[__package__].preferences

# 全域快取清單，防止 UI 渲染時文字損壞
_cached_languages = []

def build_language_cache():
    """嚴格參考原版實作：切換至 en_US 取得乾淨的語系清單"""
    global _cached_languages
    _cached_languages.clear()

    original_lang = bpy.context.preferences.view.language

    try:
        # 暫時切換到英文以獲取標準標識符，避免亂碼
        bpy.context.preferences.view.language = 'en_US'
        prop = bpy.types.PreferencesView.bl_rna.properties['language']

        for item in prop.enum_items:
            # 存儲 (標識符, 顯示名稱, 描述)
            _cached_languages.append(
                (item.identifier, item.name, item.identifier)
            )
    except Exception as e:
        print("Language cache error:", e)
        _cached_languages = [('en_US', 'English (US)', 'en_US')]
    finally:
        try:
            bpy.context.preferences.view.language = original_lang
        except:
            pass

def get_available_languages(self, context):
    """依賴快取，避免在 UI 繪製時重複執行邏輯"""
    if not _cached_languages:
        build_language_cache()
    return _cached_languages

# ==================================================
# i18n 文字翻譯 (沿用原版字典)
# ==================================================

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
    """獲取翻譯文字邏輯"""
    if lang is None:
        try:
            lang = bpy.context.preferences.view.language
        except:
            lang = 'en_US'
    if lang not in i18n_dict:
        lang = 'en_US'
    return i18n_dict[lang].get(key, i18n_dict['en_US'].get(key, key))

# ==================================================
# Operators (嚴格參考 b3d-ui-langloop.py 實作)
# ==================================================

class LANGSWITCH_OT_add_language(Operator):
    bl_idname = "langswitch.add_language"
    bl_label = "Add Language"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        prefs = get_prefs()
        if prefs.cycle_count < 10:
            prefs.cycle_count += 1
        return {'FINISHED'}

class LANGSWITCH_OT_remove_language(Operator):
    bl_idname = "langswitch.remove_language"
    bl_label = "Remove Language"
    bl_options = {'REGISTER', 'UNDO'}
    index: IntProperty()

    def execute(self, context):
        prefs = get_prefs()
        if prefs.cycle_count > 2 and self.index >= 2:
            for i in range(self.index, prefs.cycle_count - 1):
                setattr(prefs, f"language_{i}", getattr(prefs, f"language_{i + 1}"))
            prefs.cycle_count -= 1
        return {'FINISHED'}

class LANGSWITCH_OT_cycle_language(Operator):
    bl_idname = "langswitch.cycle_language"
    bl_label = "Cycle UI Language"
    bl_options = {'REGISTER'}

    def execute(self, context):
        prefs = get_prefs()
        current_lang = context.preferences.view.language
        
        lang_list = [getattr(prefs, f"language_{i}") for i in range(prefs.cycle_count)]

        try:
            idx = lang_list.index(current_lang)
            next_idx = (idx + 1) % len(lang_list)
        except ValueError:
            next_idx = 0

        target_lang = lang_list[next_idx]
        context.preferences.view.language = target_lang
        self.report({'INFO'}, f"{get_text('switch_to')} {target_lang}")
        return {'FINISHED'}

# ==================================================
# Preferences UI 排版 (嚴格參考原版排版)
# ==================================================

class LANGSWITCH_Preferences(AddonPreferences):
    bl_idname = __package__

    cycle_count: IntProperty(name="Cycle Count", default=2, min=2, max=10)

    # 語言槽位定義 (使用 EnumProperty 連結快取函數)
    language_0: EnumProperty(items=get_available_languages)
    language_1: EnumProperty(items=get_available_languages)
    language_2: EnumProperty(items=get_available_languages)
    language_3: EnumProperty(items=get_available_languages)
    language_4: EnumProperty(items=get_available_languages)
    language_5: EnumProperty(items=get_available_languages)
    language_6: EnumProperty(items=get_available_languages)
    language_7: EnumProperty(items=get_available_languages)
    language_8: EnumProperty(items=get_available_languages)
    language_9: EnumProperty(items=get_available_languages)

    def draw(self, context):
        layout = self.layout
        current_lang = context.preferences.view.language

        layout.separator()
        layout.label(text=get_text('select_languages', current_lang))
        
        # 嚴格參考原版 box 排版與 icon 設置
        box = layout.box()
        for i in range(self.cycle_count):
            row = box.row(align=True)
            
            # 刪除按鈕欄位
            btn_col = row.column(align=False)
            if i < 2: btn_col.enabled = False
            remove_op = btn_col.operator("langswitch.remove_language", text="", icon='REMOVE')
            remove_op.index = i

            # 語系選擇欄位
            space = "\u0020"
            row.prop(self, f"language_{i}", text=f"{space}{get_text('language', current_lang)} {i+1} ")

        if self.cycle_count < 10:
            row = box.row()
            row.operator("langswitch.add_language", text="", icon='ADD')
        
        layout.separator()
        layout.label(text=get_text('shortcut_hint', current_lang))

# ==================================================
# Register
# ==================================================

addon_keymaps = []

def register():
    # 註冊順序與快取建立
    bpy.utils.register_class(LANGSWITCH_OT_add_language)
    bpy.utils.register_class(LANGSWITCH_OT_remove_language)
    bpy.utils.register_class(LANGSWITCH_OT_cycle_language)
    bpy.utils.register_class(LANGSWITCH_Preferences)

    # 在註冊時建立快取，確保標籤名稱正確
    build_language_cache()

    # 註冊快速鍵
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

    bpy.utils.unregister_class(LANGSWITCH_Preferences)
    bpy.utils.unregister_class(LANGSWITCH_OT_cycle_language)
    bpy.utils.unregister_class(LANGSWITCH_OT_remove_language)
    bpy.utils.unregister_class(LANGSWITCH_OT_add_language)