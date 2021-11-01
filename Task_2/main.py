import os
import win32security
import ntsecuritycon as con

fname1 = "temp1.txt"
fname2 = "temp2.txt"


# Отображение разрешений пользователей к файлу
def show_cacls(filename):
    for line in os.popen("cacls %s" % filename).read().splitlines():
        print(line)


# имена пользователей
admin, domain, type = win32security.LookupAccountName("", "krule")
user, domain, type = win32security.LookupAccountName("", "user2")


def set_ace(fname, ace_for_admin, ace_for_user):
    sd = win32security.GetFileSecurity(fname, win32security.DACL_SECURITY_INFORMATION)
    dacl = win32security.ACL()

    ace_count = dacl.GetAceCount()
    # удаляем старые разрешения
    for i in range(ace_count):
        dacl.DeleteAce(0)

    # если передано не пустое значение, устанавливаем новые разрешения
    if ace_for_admin:
        dacl.AddAccessAllowedAce(win32security.ACL_REVISION, ace_for_admin, admin)
    if ace_for_user:
        dacl.AddAccessAllowedAce(win32security.ACL_REVISION, ace_for_user, user)

    sd.SetSecurityDescriptorDacl(1, dacl, 0)
    win32security.SetFileSecurity(fname, win32security.DACL_SECURITY_INFORMATION, sd)

# Первоначальные разрешения
print("Было: ")
show_cacls(fname1)
show_cacls(fname2)
# Задаем новые разрешения
set_ace(fname1, "", con.FILE_ALL_ACCESS)
set_ace(fname2, con.FILE_ALL_ACCESS, "")
# Вывод новых разрешений
print("Стало: ")
show_cacls(fname1)
show_cacls(fname2)
