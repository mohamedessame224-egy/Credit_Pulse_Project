"""
Credit Pulse - Translation Utility
Bilingual Arabic/English support
"""
from flask import session

TRANSLATIONS = {
    # Navigation
    'nav_home': {'ar': 'الرئيسية', 'en': 'Home'},
    'nav_survey': {'ar': 'الاستبيان', 'en': 'Survey'},
    'nav_admin': {'ar': 'لوحة التحكم', 'en': 'Admin Dashboard'},
    'nav_logout': {'ar': 'تسجيل الخروج', 'en': 'Logout'},

    # Welcome page
    'welcome_title': {'ar': 'مرحباً بك في Credit Pulse', 'en': 'Welcome to Credit Pulse'},
    'welcome_subtitle': {'ar': 'منصة استبيانات قطاع الائتمان', 'en': 'Credit Sector Survey Platform'},
    'welcome_bank': {'ar': 'البنك الأهلي المصري', 'en': 'National Bank of Egypt'},
    'welcome_desc': {'ar': 'نسعى إلى تطوير بيئة العمل وتحسين الأداء من خلال الاستماع إلى آراء موظفينا الكرام.', 'en': 'We strive to develop the work environment and improve performance by listening to our valued employees.'},
    'welcome_time': {'ar': 'الوقت المقدر للإجابة:', 'en': 'Estimated completion time:'},
    'welcome_minutes': {'ar': 'دقائق', 'en': 'minutes'},
    'welcome_start': {'ar': 'ابدأ الاستبيان', 'en': 'Start Survey'},
    'welcome_confidential': {'ar': '🔒 إجاباتك سرية ومحمية تماماً', 'en': '🔒 Your responses are completely confidential and protected'},
    'welcome_anonymous': {'ar': 'يمكنك المشاركة بشكل مجهول', 'en': 'You can participate anonymously'},

    # Employee info page
    'info_title': {'ar': 'معلوماتك الشخصية', 'en': 'Your Information'},
    'info_subtitle': {'ar': 'الحقل الإلزامي الوحيد هو القسم', 'en': 'The only required field is your department'},
    'info_dept': {'ar': 'القسم *', 'en': 'Department *'},
    'info_dept_select': {'ar': 'اختر القسم', 'en': 'Select Department'},
    'info_name': {'ar': 'الاسم (اختياري)', 'en': 'Name (Optional)'},
    'info_id': {'ar': 'الرقم الوظيفي (اختياري)', 'en': 'Employee ID (Optional)'},
    'info_anonymous': {'ar': 'المشاركة بشكل مجهول', 'en': 'Participate Anonymously'},
    'info_anonymous_note': {'ar': 'لن يتم حفظ اسمك أو رقمك الوظيفي', 'en': 'Your name and ID will not be saved'},
    'info_next': {'ar': 'التالي', 'en': 'Next'},
    'info_required': {'ar': 'يرجى اختيار القسم', 'en': 'Please select your department'},

    # Survey page
    'survey_section': {'ar': 'القسم', 'en': 'Section'},
    'survey_of': {'ar': 'من', 'en': 'of'},
    'survey_question': {'ar': 'سؤال', 'en': 'Question'},
    'survey_progress': {'ar': 'التقدم', 'en': 'Progress'},
    'survey_next': {'ar': 'التالي', 'en': 'Next'},
    'survey_prev': {'ar': 'السابق', 'en': 'Previous'},
    'survey_submit': {'ar': 'إرسال الاستبيان', 'en': 'Submit Survey'},
    'survey_required_msg': {'ar': 'يرجى الإجابة على جميع الأسئلة الإلزامية', 'en': 'Please answer all required questions'},
    'survey_rating_label': {'ar': 'التقييم (1-5)', 'en': 'Rating (1-5)'},
    'survey_comment_placeholder': {'ar': 'اكتب تعليقك هنا...', 'en': 'Write your comment here...'},

    # Rating labels
    'rating_1': {'ar': 'ضعيف جداً', 'en': 'Very Poor'},
    'rating_2': {'ar': 'ضعيف', 'en': 'Poor'},
    'rating_3': {'ar': 'مقبول', 'en': 'Fair'},
    'rating_4': {'ar': 'جيد', 'en': 'Good'},
    'rating_5': {'ar': 'ممتاز', 'en': 'Excellent'},

    # Thank you page
    'thanks_title': {'ar': 'شكراً لمشاركتك!', 'en': 'Thank You for Participating!'},
    'thanks_subtitle': {'ar': 'تم إرسال إجاباتك بنجاح', 'en': 'Your responses have been submitted successfully'},
    'thanks_message': {'ar': 'نقدر مساهمتك في تطوير بيئة العمل. سيتم مراجعة إجاباتك باهتمام بالغ.', 'en': 'We appreciate your contribution to improving the work environment. Your responses will be carefully reviewed.'},
    'thanks_home': {'ar': 'العودة للرئيسية', 'en': 'Return to Home'},

    # Admin
    'admin_title': {'ar': 'لوحة تحكم Credit Pulse', 'en': 'Credit Pulse Dashboard'},
    'admin_login_title': {'ar': 'تسجيل دخول المدير', 'en': 'Admin Login'},
    'admin_username': {'ar': 'اسم المستخدم', 'en': 'Username'},
    'admin_password': {'ar': 'كلمة المرور', 'en': 'Password'},
    'admin_login_btn': {'ar': 'تسجيل الدخول', 'en': 'Login'},
    'admin_login_error': {'ar': 'اسم المستخدم أو كلمة المرور غير صحيحة', 'en': 'Invalid username or password'},

    # Dashboard cards
    'card_total': {'ar': 'إجمالي المشاركين', 'en': 'Total Participants'},
    'card_depts': {'ar': 'الأقسام المشاركة', 'en': 'Participating Departments'},
    'card_satisfaction': {'ar': 'متوسط الرضا', 'en': 'Avg. Satisfaction'},
    'card_pulse_score': {'ar': 'نقاط Credit Pulse', 'en': 'Credit Pulse Score'},
    'card_anonymous': {'ar': 'مشاركات مجهولة', 'en': 'Anonymous Responses'},

    # Reports
    'report_excel': {'ar': 'تقرير Excel', 'en': 'Excel Report'},
    'report_pdf': {'ar': 'تقرير PDF', 'en': 'PDF Report'},
    'report_word': {'ar': 'تقرير Word', 'en': 'Word Report'},
    'report_generate': {'ar': 'إنشاء التقرير', 'en': 'Generate Report'},

    # Language
    'lang_switch': {'ar': 'English', 'en': 'العربية'},
    'lang_current': {'ar': 'ar', 'en': 'en'},

    # General
    'error_404': {'ar': 'الصفحة غير موجودة', 'en': 'Page Not Found'},
    'error_500': {'ar': 'خطأ في الخادم', 'en': 'Server Error'},
    'go_home': {'ar': 'العودة للرئيسية', 'en': 'Go Home'},
}


def get_lang():
    return session.get('lang', 'ar')


def t(key):
    lang = get_lang()
    if key in TRANSLATIONS:
        return TRANSLATIONS[key].get(lang, TRANSLATIONS[key].get('ar', key))
    return key


def get_all_translations():
    lang = get_lang()
    return {k: v.get(lang, v.get('ar', k)) for k, v in TRANSLATIONS.items()}
