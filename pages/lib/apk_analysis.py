import os
from django.conf import settings
from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.dvm import DalvikVMFormat
from qark.scanner.scanner import Scanner
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from lxml import etree


def apk_anaysis(path:str):
    a = APK(path)
    scanner = Scanner(manifest_path=path,path_to_source=path)
    scanner.run()
    issues = scanner.issues

    certifications = []

    certificates_der = a.get_certificates_der_v3()
    for cert_der in certificates_der:
        parse = parse_certificate(cert_der)
        certifications.append(parse)

    analysis = {
        "package_name": a.get_package(),
        "app_name": a.get_app_name(),
        "android_version": a.get_androidversion_name(),
        "android_version_2": a.get_androidversion_code(),
        "min_sdk": a.get_min_sdk_version(),
        "target_sdk_version": a.get_target_sdk_version(),
        "permission": a.get_permissions(),
        "activites": a.get_activities(),
        "services": a.get_services(),
        "receivers": a.get_receivers(),
        "manifest": a.get_android_manifest_xml(),
        "certificate": certifications,
        "resource": a.get_android_resources(),
        "issues": issues,
    }

    try:
        os.remove(path)
    except:
        print('Error while deleting file')
    return analysis

def parse_certificate(cert_der):
    cert = x509.load_der_x509_certificate(cert_der, default_backend())
    subject = cert.subject
    issuer = cert.issuer
    return subject, issuer