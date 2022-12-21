{
    'name': 'Payroll Fuelboss doo Zenica',
    'version': '1.0',
    'author': "bring.out Sarajevo, BiH",
    'category': 'Human Resources/Payroll',
    'sequence': 190,
    'summary': 'Bosnian Payroll data (FBiH) company FuelBoss doo Zenica',
    'depends': ["hr", "hr_contract", "payroll", "base_address_extended", "l10n_bs"],
    'data': [
        "data/hr_payroll_rules.xml",
        "data/hr_payroll_rules_dopr_iz.xml",
        "data/hr_payroll_rules_dopr_na.xml",
        "data/hr_payroll_rules_dopr_iz_na.xml",
        "data/hr_payroll_rules_detas.xml",
        "data/hr_payroll_rules_end.xml",
        "data/hr_payroll_rules_delete.xml",
        #"data/test.xml"
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'GPL-3',
}
