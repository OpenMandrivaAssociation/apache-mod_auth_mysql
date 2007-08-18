#Module-Specific definitions
%define apache_version 2.2.4
%define mod_name mod_auth_mysql
%define mod_conf 12_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Basic authentication for the apache web server using a MySQL database
Name:		apache-%{mod_name}
Version:	3.0.0
Release:	%mkrel 12
Group:		System/Servers
License:	Apache License
URL:		http://sourceforge.net/projects/modauthmysql/
Source0:	http://prdownloads.sourceforge.net/modauthmysql/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}
Patch0:		mod_auth_mysql-3.0.0-apr1x.patch
Patch1:		mod_auth_mysql-3.0.0-htpasswd-style.diff
BuildRequires:	mysql-devel
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
mod_auth_mysql is an Apache module to authenticate users and authorize access
through a MySQL database. It is flexible and support several encryption
methods.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p1 -b .apr1x
%patch1 -p0 -b .htpasswd-style

cp %{SOURCE1} %{mod_conf}

%build

%{_sbindir}/apxs -L%{_libdir}/mysql -I%{_includedir}/mysql -Wl,-lmysqlclient -c mod_auth_mysql.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc BUILD CHANGES CONFIGURE README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
