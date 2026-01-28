# -*- coding: utf-8 -*-


import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import IntProperty, EnumProperty
from bpy.app.handlers import persistent

bl_info = {
    "name": "B3D UI Language Loop",
    "author": "楊景貴 / issac",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "Edit > Preferences > Add-ons",
    "description": "Quick language switching for Blender interface",
    "category": "Interface",
}

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
        'shortcut_hint': "Nastavení zkratek: Upravit > Předvolby > Klávesové zkratky > Hledat 'b3d-ui-langloop'",
        'switch_to': "Jazyk změněn na:",
        'current_shortcut': "Aktuální zkratka: {key}",
        'shortcut_missing': "Chybí (viz manuál)",
    },
    'tr_TR': {
        'cycle_count': "Döngü sayısı",
        'cycle_count_desc': "Geçiş yapılacak dil sayısı",
        'language': "Dil",
        'select_languages': "Geçiş yapılacak dilleri seçin:",
        'shortcut_hint': "Kısayol ayarları: Düzenle > Tercihler > Tuş Haritalama > 'b3d-ui-langloop' ara",
        'switch_to': "Dil değiştirildi:",
        'current_shortcut': "Mevcut kısayol: {key}",
        'shortcut_missing': "Eksik (lütfen kılavuza bakın)",
    },
    'ar_EG': {
        'cycle_count': "عدد الدورات",
        'cycle_count_desc': "عدد اللغات للتبديل بينها",
        'language': "اللغة",
        'select_languages': "حدد اللغات للتبديل بينها:",
        'shortcut_hint': "إعدادات الاختصارات: تحرير > التفضيلات > خريطة المفاتيح > ابحث عن 'b3d-ui-langloop'",
        'switch_to': "تم التبديل إلى اللغة:",
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

def _(key: str) -> str:
    lang = bpy.context.preferences.view.language
    return i18n_dict.get(lang, i18n_dict["en_US"]).get(key, i18n_dict["en_US"].get(key, key))


_language_cache = []

def build_language_cache():
    global _language_cache
    _language_cache.clear()
    original_lang = bpy.context.preferences.view.language

    try:
        bpy.context.preferences.view.language = "en_US"
        enum_items = bpy.types.PreferencesView.bl_rna.properties["language"].enum_items

        for item in enum_items:
            _language_cache.append((item.identifier, item.name, item.identifier))

    finally:
        bpy.context.preferences.view.language = original_lang

def available_languages(self, context):

    if not _language_cache:
        build_language_cache()
    return _language_cache


class B3D_LANGLOOP_Preferences(AddonPreferences):
    bl_idname = __package__
    cycle_count= IntProperty(
        name=lambda _: _("cycle_count"),
        description=lambda _: _("cycle_count_desc"),
        default=2,
        min=2,
        max=10,
    )
    language_0= EnumProperty(name="Language 1", items=available_languages)
    language_1= EnumProperty(name="Language 2", items=available_languages)
    language_2= EnumProperty(name="Language 3", items=available_languages)
    language_3= EnumProperty(name="Language 4", items=available_languages)
    language_4= EnumProperty(name="Language 5", items=available_languages)
    language_5= EnumProperty(name="Language 6", items=available_languages)
    language_6= EnumProperty(name="Language 7", items=available_languages)
    language_7= EnumProperty(name="Language 8", items=available_languages)
    language_8= EnumProperty(name="Language 9", items=available_languages)
    language_9= EnumProperty(name="Language 10", items=available_languages)

    def draw(self, context):
        layout = self.layout
        layout.label(text=_("select_languages"))
        box = layout.box()

        for i in range(self.cycle_count):
            box.prop(self, f"language_{i}", text=f'{_("language")} {i + 1}')
        layout.separator()
        layout.label(text=_("shortcut_hint"))

class B3D_LANGLOOP_OT_cycle(Operator):
    bl_idname = "b3d_langloop.cycle_language"
    bl_label = "Cycle UI Language"

    def execute(self, context):
        prefs = context.preferences.addons[__package__].preferences
        current = context.preferences.view.language
        languages = [
            getattr(prefs, f"language_{i}")

            for i in range(prefs.cycle_count)

            if getattr(prefs, f"language_{i}", None)
        ]

        if not languages:
            return {"CANCELLED"}

        next_index = (languages.index(current) + 1) % len(languages) if current in languages else 0
        context.preferences.view.language = languages[next_index]
        self.report({"INFO"}, f"{_('switch_to')} {languages[next_index]}")
        return {"FINISHED"}


classes = (
    B3D_LANGLOOP_Preferences,
    B3D_LANGLOOP_OT_cycle,
)

addon_keymaps = []

def register():

    for cls in classes:
        bpy.utils.register_class(cls)
    build_language_cache()
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps.new(name="Window", space_type="EMPTY")
        kmi = km.keymap_items.new(
            B3D_LANGLOOP_OT_cycle.bl_idname,
            type="T",
            value="PRESS",
            ctrl=True,
            alt=True,
            shift=True,
        )
        addon_keymaps.append((km, kmi))

def unregister():

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)