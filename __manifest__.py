{
    'name': 'Payroll Fuelboss doo Zenica',
    'version': '1.1',
    'author': "bring.out Sarajevo, BiH",
    'category': 'Human Resources/Payroll',
    'sequence': 190,
    'summary': 'Bosnian Payroll data (FBiH) company FuelBoss doo Zenica',
    'depends': ["hr", "hr_contract", "payroll", "base_address_extended", "l10n_bs", "l10n_bs_hr_timesheet"],
    'data': [
        "data/hr_payroll_rules.xml",
        "data/hr_payroll_contrib_register.xml",
        "data/hr_payroll_category.xml",
        "data/hr_payroll_leve_type.xml",
        "data/hr_payroll_rule_param.xml",
        "data/hr_payroll_rules_dopr_iz.xml",
        "data/hr_payroll_rules_dopr_na.xml",
        "data/hr_payroll_rules_dopr_iz_na.xml",
        "data/hr_payroll_rules_detas.xml",
        "data/hr_payroll_rules_end.xml",
        "data/hr_payroll_fb_sistematizacija.xml",
        #"data/hr_payroll_rules_delete.xml",
        "data/res.bank.csv",
        "views/employee_code.xml",
        "views/employee_tree_view.xml",
        "views/project_task_sihtarica_default.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'GPL-3',
}
