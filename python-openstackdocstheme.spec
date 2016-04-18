%if 0%{?fedora}
%global with_python3 1
%endif

%global pypi_name openstackdocstheme

Name:           python-%{pypi_name}
Version:        1.3.0
Release:        1%{?dist}
Summary:        OpenStack Docs Theme

License:        ASL 2.0
URL:            http://docs.openstack.org/
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Patch0001:      0001-Remove-all-Google-Analytics-tracking.patch
Patch0002:      0002-Remove-external-references.patch
BuildArch:      noarch

%package -n     python2-%{pypi_name}
Summary:        OpenStack Docs Theme
%{?python_provide:%python_provide python2-%{pypi_name}}
Provides:       bundled(js-jquery)

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr >= 1.8
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  git

Requires: python-pbr
Requires: python-requests

%description -n python2-%{pypi_name}
OpenStack docs.openstack.org Sphinx Theme

Theme and extension support for Sphinx documentation that is published to
docs.openstack.org. Intended for use by OpenStack projects.

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        OpenStack Docs Theme
%{?python_provide:%python_provide python3-%{pypi_name}}
Provides:       bundled(js-jquery)

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 1.8
BuildRequires:  python3-sphinx
BuildRequires:  python3-oslo-sphinx
BuildRequires:  git

Requires: python3-pbr
Requires: python3-requests

%description -n python3-%{pypi_name}
OpenStack docs.openstack.org Sphinx Theme

Theme and extension support for Sphinx documentation that is published to
docs.openstack.org. Intended for use by OpenStack projects.
%endif

%package -n python-%{pypi_name}-doc
Summary:        openstackdocstheme documentation
%description -n python-%{pypi_name}-doc
Documentation for openstackdocstheme

%description
OpenStack docs.openstack.org Sphinx Theme

Theme and extension support for Sphinx documentation that is published to
docs.openstack.org. Intended for use by OpenStack projects.

%prep
%autosetup -n %{pypi_name}-%{version} -p1

%build
# Make sure there is no Google Analytics
sed -i 's/analytics_tracking_code.*/analytics_tracking_code\ =/' openstackdocstheme/theme/openstackdocs/theme.conf

%py2_build
%if 0%{?with_python3}
%py3_build
%endif
# generate html docs
PYTHONPATH=. sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install


%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%files -n python-%{pypi_name}-doc
%doc html

%changelog
* Mon Apr 18 2016 Javier Peña <jpena@redhat.com> - 1.3.0-1
- Bumped to upstream release 1.3.0

* Thu Mar 03 2016 Javier Peña <jpena@redhat.com> - 1.2.7-2
- Fixed prep section
- Removed unneeded comments
- Added bundled(js-jquery) to provides

* Thu Mar 03 2016 jpena <jpena@redhat.com> - 1.2.7-1
- Initial package.
