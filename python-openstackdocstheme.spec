%if 0%{?fedora}
%global with_python3 1
%endif

%global pypi_name openstackdocstheme

Name:           python-%{pypi_name}
Version:        1.11.0
Release:        1%{?dist}
Summary:        OpenStack Docs Theme

License:        ASL 2.0
URL:            http://docs.openstack.org/
Source0:        https://pypi.io/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
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
BuildRequires:  git

Requires: python-pbr
Requires: python-requests
Requires: python-sphinx >= 1.6.2

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
BuildRequires:  git

Requires: python3-pbr
Requires: python3-requests
Requires: python3-sphinx >= 1.6.2

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
%autosetup -n %{pypi_name}-%{version} -p1 -S git

%build
# Make sure there is no Google Analytics
sed -i 's/analytics_tracking_code.*/analytics_tracking_code\ =/' openstackdocstheme/theme/openstackdocs/theme.conf
# Prevent doc build warnings from causing a build failure
sed -i '/warning-is-error/d' setup.cfg

%py2_build
%if 0%{?with_python3}
%py3_build
%endif
# generate html docs
python setup.py build_sphinx
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
%doc doc/build/html

%changelog
* Wed Jun 28 2017 Javier Peña <jpena@redhat.com> - 1.11.0-1
- Updated to upstream release 1.11.0 (bz#1435494)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.5.0-2
- Rebuild for Python 3.6

* Thu Sep 22 2016 Javier Peña <jpena@redhat.com> - 1.5.0-1
- Bumped to upstream release 1.5.0

* Fri Aug 19 2016 Javier Peña <jpena@redhat.com> - 1.4.0-2
- Use sphinx-build-2 for doc generation, there are issues with the Python3 version

* Fri Aug 19 2016 Javier Peña <jpena@redhat.com> - 1.4.0-1
- Bumped to upstream release 1.4.0
- Fixed source URL

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Apr 18 2016 Javier Peña <jpena@redhat.com> - 1.3.0-1
- Bumped to upstream release 1.3.0

* Thu Mar 03 2016 Javier Peña <jpena@redhat.com> - 1.2.7-2
- Fixed prep section
- Removed unneeded comments
- Added bundled(js-jquery) to provides

* Thu Mar 03 2016 jpena <jpena@redhat.com> - 1.2.7-1
- Initial package.
