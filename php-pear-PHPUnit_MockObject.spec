%define  upstream_name PHPUnit_MockObject
%define peardir %(pear config-get php_dir 2> /dev/null || echo %{_datadir}/pear)
%define xmldir  /var/lib/pear

Summary: 	Mock Object library for PHPUnit
Name: 		php-pear-%{upstream_name}
Version: 	1.2.3
Release: 	2
License: 	BSD
Group: 		Development/PHP
Source0: 	http://pear.phpunit.de/get/PHPUnit_MockObject-%{version}.tgz
URL: 		https://pear.phpunit.de/package/PHPUnit_MockObject
BuildRequires: 	php-pear >= 1.4.7
BuildRequires: 	php-channel-phpunit
Requires: 	php-pear-Text_Template >= 1.1.1
Requires:	php-pear >= 1.9.4
Requires: 	php-channel-phpunit
BuildArch: 	noarch

%description
Mock Object library for PHPUnit

%prep
%setup -c -T
pear -v -c pearrc \
        -d php_dir=%{peardir} \
        -d doc_dir=/docs \
        -d bin_dir=%{_bindir} \
        -d data_dir=%{peardir}/data \
        -d test_dir=%{peardir}/tests \
        -d ext_dir=%{_libdir} \
        -s

%build

%install
rm -rf %{buildroot}
pear -c pearrc install --nodeps --packagingroot %{buildroot} %{SOURCE0}
        
# Clean up unnecessary files
rm pearrc
rm %{buildroot}/%{peardir}/.filemap
rm %{buildroot}/%{peardir}/.lock
rm -rf %{buildroot}/%{peardir}/.registry
rm -rf %{buildroot}%{peardir}/.channels
rm %{buildroot}%{peardir}/.depdb
rm %{buildroot}%{peardir}/.depdblock

mv %{buildroot}/docs .


# Install XML package description
mkdir -p %{buildroot}%{xmldir}
tar -xzf %{SOURCE0} package.xml
cp -p package.xml %{buildroot}%{xmldir}/PHPUnit_MockObject.xml

%clean
rm -rf %{buildroot}

%post
pear install --nodeps --soft --force --register-only %{xmldir}/PHPUnit_MockObject.xml

%postun
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only pear.phpunit.de/PHPUnit_MockObject
fi

%files
%defattr(-,root,root)
%doc docs/PHPUnit_MockObject/*
%{peardir}/*
%{xmldir}/PHPUnit_MockObject.xml


%changelog
* Tue Mar 27 2012 Thomas Spuhler <tspuhler@mandriva.org> 1.1.1-2mdv2012.0
+ Revision: 787367
- rebuilt

* Sat Mar 17 2012 Thomas Spuhler <tspuhler@mandriva.org> 1.1.1-1
+ Revision: 785452
- upgrade to 1.1.1
  pearize specfile

* Fri Dec 16 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-2
+ Revision: 742185
- fix major breakage by careless packager

* Wed Nov 16 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-1
+ Revision: 730887
- import php-pear-PHPUnit_MockObject


* Wed Nov 16 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-1mdv2010.2
- initial Mandriva package
