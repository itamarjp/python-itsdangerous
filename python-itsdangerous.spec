%global srcname itsdangerous

Name:           python-itsdangerous
Version:        0.11
Release:        1%{?dist}
Summary:        Python library for passing trusted data to untrusted environments
Group:          Development/Languages
License:        BSD
URL:            http://packages.python.org/itsdangerous/
#Source0:        http://pypi.python.org/packages/source/i/%{srcname}/%{srcname}-%{version}.tar.gz
# Tarballs on PyPi lack LICENSE and tests, so we generate our own from git instead:
# git archive --format=tar --prefix=itsdangerous-0.11/ 0.11 | xz >itsdangerous-git-0.11.tar.xz
Source0:        %{srcname}-git-%{version}.tar.xz
BuildArch:      noarch
BuildRequires:  python-setuptools-devel

%description

%prep
%setup -q -n %{srcname}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%check
PYTHONPATH=$RPM_BUILD_ROOT%{python_sitelib} %{__python} tests.py

%files
%doc LICENSE CHANGES README
%{python_sitelib}/itsdangerous*

%changelog
* Wed Nov 11 2011 Dan Callaghan <dcallagh@redhat.com> - 0.11-1
- initial version
