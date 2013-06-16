%global upstream_name itsdangerous

%if 0%{?fedora} || 0%{?rhel} > 6
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{upstream_name}
Version:        0.21
Release:        2%{?dist}
Summary:        Python library for passing trusted data to untrusted environments
License:        BSD
URL:            http://pythonhosted.org/itsdangerous/
Source0:        http://pypi.python.org/packages/source/i/%{upstream_name}/%{upstream_name}-%{version}.tar.gz
# Tarballs on PyPi lack LICENSE, CHANGES, and tests.
# https://github.com/mitsuhiko/itsdangerous/pull/22
Source1:        LICENSE
Source2:        CHANGES
Source3:        tests.py
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
Itsdangerous is a Python library for passing data through untrusted 
environments (for example, HTTP cookies) while ensuring the data is not 
tampered with.

Internally itsdangerous uses HMAC and SHA1 for signing by default and bases the 
implementation on the Django signing module. It also however supports JSON Web 
Signatures (JWS).

%if %{with python3}
%package -n python3-%{upstream_name}
Summary:        Python 3 library for passing trusted data to untrusted environments

%description -n python3-%{upstream_name}
Itsdangerous is a Python 3 library for passing data through untrusted 
environments (for example, HTTP cookies) while ensuring the data is not 
tampered with.

Internally itsdangerous uses HMAC and SHA1 for signing by default and bases the 
implementation on the Django signing module. It also however supports JSON Web 
Signatures (JWS).
%endif

%prep
%setup -q -n %{upstream_name}-%{version}
rm -r *.egg-info
cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} .

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%check
PYTHONPATH=%{buildroot}%{python_sitelib} %{__python} tests.py

%if %{with python3}
pushd %{py3dir}
PYTHONPATH=%{buildroot}%{python3_sitelib} %{__python3} tests.py
popd
%endif

%files
%doc LICENSE CHANGES README
%{python_sitelib}/%{upstream_name}.py*
%{python_sitelib}/%{upstream_name}*.egg-info

%if %{with python3}
%files -n python3-%{upstream_name}
%doc LICENSE CHANGES README
%{python3_sitelib}/%{upstream_name}.py
%{python3_sitelib}/%{upstream_name}*.egg-info
%{python3_sitelib}/__pycache__/%{upstream_name}*
%endif

%changelog
* Mon Jun 17 2013 Dan Callaghan <dcallagh@redhat.com> - 0.21-2
- $RPM_BUILD_ROOT -> %%{buildroot}

* Fri Jun 14 2013 Dan Callaghan <dcallagh@redhat.com> - 0.21-1
- updated to upstream release 0.21
- added Python 3 subpackage

* Wed Nov 16 2011 Dan Callaghan <dcallagh@redhat.com> - 0.11-1
- initial version
