%define with_ldap 1
%define upstream_name z-push

Summary:	ActiveSync over-the-air implementation for Zarafa
Name:		zarafa-z-push
Version:	2.2.5
Release:	1%{?dist}
License:	AGPLv3 with exceptions
Group:		Applications/Productivity
URL:		http://z-push.sourceforge.net/
Source0:	http://download.berlios.de/%{upstream_name}/%{upstream_name}-%{version}.tar.gz
Source1:	zarafa-z-push.conf
Source2:	zarafa-z-push.logrotate
Patch1:		z-push-2.0-zarafa.patch
Patch2:		z-push-2.2.0-1934-migrate21to22.patch
Requires:	httpd, php >= 5.1.0, php-process >= 5.1.0
# Kludgy: Zarafa binaries are messy, so disable these deps for repoclosure
# Requires: php-mapi >= 7.0.0, zarafa-common >= 7.0.5
%if %{with_ldap}
Requires:	php-ldap >= 5.1.0
%endif
BuildArch:	noarch

%description
Z-Push is an implementation of the ActiveSync protocol which is used
'over-the-air' for multi platform ActiveSync devices, including Windows
Mobile, Android, iPhone, Sony Ericsson and Nokia mobile devices. With
Z-Push any groupware can be connected and synced with these devices.

This package is prepared for use with the Zarafa Collaboration Platform
and Open Source Collaboration. For non-Zarafa use cases, please use the
regular Z-Push package.

%prep
%setup -q -n %{upstream_name}-%{version}
%patch1 -p1 -b .zarafa
%patch2 -p1 -b .migrate

%build

%install
rm -rf $RPM_BUILD_ROOT

# Create all needed directories
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/{{,zarafa}/%{upstream_name},httpd/conf.d,logrotate.d}/
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/{%{name},%{name}}}/
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/{%{name},%{name}}/state/
# Create the default log directory for packaging
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/%{upstream_name}/

# Install all files into destination
cp -af * $RPM_BUILD_ROOT%{_datadir}/%{name}/

# Move configuration file to its place
mv -f $RPM_BUILD_ROOT%{_datadir}/%{name}/config.php $RPM_BUILD_ROOT%{_sysconfdir}/zarafa/%{upstream_name}/config.php
ln -sf ../../..%{_sysconfdir}/zarafa/%{upstream_name}/config.php $RPM_BUILD_ROOT%{_datadir}/%{name}/config.php

# Install the apache configuration file
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Install logrotate
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zarafa-z-push

# Remove all non-Zarafa related files
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/backend/{diffbackend,imap,maildir,vcarddir}.php

# Move searchldap configuration to its place
%if %{with_ldap}
mv -f $RPM_BUILD_ROOT%{_datadir}/%{name}/backend/searchldap/config.php $RPM_BUILD_ROOT%{_sysconfdir}/zarafa/%{upstream_name}/searchldap.php
ln -sf ../../../../..%{_sysconfdir}/zarafa/%{name}/searchldap.php $RPM_BUILD_ROOT%{_datadir}/%{name}/backend/searchldap/config.php
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/backend/{searchbackend.php,searchldap/}
%endif

# Install Zarafa-related command line tool
install -p -m 755 z-push-admin.php $RPM_BUILD_ROOT%{_bindir}/z-push-admin

# Remove all unwanted files and directories
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/{INSTALL,LICENSE,{config,debug}.php.{package,zarafa}}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/service httpd condrestart >/dev/null 2>&1
exit 0

%pre
# Remove state if exists to prevent upgrade problems
rm -rf /var/lib/zarafa-z-push/state/ > /dev/null 2>&1 

%files
%defattr(-,root,root,-)
%doc LICENSE
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/zarafa-z-push
%dir %{_sysconfdir}/zarafa/%{upstream_name}/
%config(noreplace) %{_sysconfdir}/zarafa/%{upstream_name}/config.php
%if %{with_ldap}
%config(noreplace) %{_sysconfdir}/zarafa/%{upstream_name}/searchldap.php
%endif
%{_bindir}/z-push-admin
%{_datadir}/%{name}/
%dir %{_localstatedir}/lib/%{name}/
%attr(-,apache,apache) %dir %{_localstatedir}/lib/%{name}/state/
%dir %attr(0775,apache,root) %{_localstatedir}/log/%{upstream_name}/

%changelog
* Wed Oct 28 2015 ClearFoundation <developer@clearfoundation.com> 2.2.5-1
- Update to 2.2.5

* Tue Feb 24 2015 ClearFoundation <developer@clearfoundation.com> 2.2.0-1
- Update to 2.2.0

* Wed Nov 12 2014 ClearFoundation <developer@clearfoundation.com> 2.1.3-1
- Update to 2.1.3

* Tue Jun 24 2014 ClearFoundation <developer@clearfoundation.com> 2.1.2-1
- Update to 2.1.2

* Mon Jun 23 2014 ClearFoundation <developer@clearfoundation.com> 2.0.9-1
- Update to 2.0.9

* Wed Aug 07 2013 ClearFoundation <developer@clearfoundation.com> 2.0.7-1
- Update to 2.0.7

* Fri Oct 26 2012 ClearFoundation <developer@clearfoundation.com> 2.0.4-3
- Add logrotate
- Clean up extra source files

* Fri Oct 19 2012 ClearFoundation <developer@clearfoundation.com> 2.0.4-1
- Remove generic z-push packaging, but keep paths consistent with original
- Update to 2.0.4

* Wed Jul 25 2012 Tim Burgess <timb80@yahoo.com> 2.0.1-2
- Remove webconfig apache paths to keep compatible with ClearOS 6.2+

* Sat Jul 14 2012 Tim Burgess <timb80@yahoo.com> 2.0.1-1
- Update to 2.0.1

* Sun Jul 01 2012 Tim Burgess <timb80@yahoo.com> 2.0-2
- Update to 2.0 final release

* Sun Jun 17 2012 Tim Burgess <timb80@yahoo.com> 2.0RC-1
- Update to 2.0RC

* Fri Mar 16 2012 Tim Burgess <timb80@yahoo.com> 2.0beta2
- Update to 2.0beta2

* Tue Feb 14 2012 Tim Burgess <timb80@yahoo.com> 2.0beta1
- Update to 2.0beta1

* Thu Oct 13 2011 Tim Burgess <timb80@yahoo.com> 2.0alpha2-1
- Update to 2.0alpha2

* Thu Oct 13 2011 Tim Burgess <timb80@yahoo.com> 1.5.5-1
- Update to 1.5.5

* Thu Jun 16 2011 Tim Burgess <timb80@yahoo.com> 1.5.3-1
- Upgrade to 1.5.3

* Tue Jun 14 2011 Tim Burgess <timb80@yahoo.com> 1.5.1-2
- Amend paths for ClearOS webconfig

* Fri Feb 11 2011 Robert Scheck <robert@fedoraproject.org> 1.5.1-1
- Upgrade to 1.5.1

* Mon Jan 26 2011 Robert Scheck <robert@fedoraproject.org> 1.5-1
- Upgrade to 1.5

* Thu May 27 2010 Robert Scheck <robert@fedoraproject.org> 1.3-2
- Use date_default_timezone_get() as default (RHBZ #570398)

* Mon May 17 2010 Robert Scheck <robert@fedoraproject.org> 1.3-1
- Upgrade to 1.3

* Sat Feb 27 2010 Robert Scheck <robert@fedoraproject.org> 1.2.2-3
- Use the equivalent namespaces as zarafa-webaccess package

* Sun Aug 09 2009 Robert Scheck <robert@fedoraproject.org> 1.2.2-2
- Require httpd instead of webserver at runtime (RFBZ #585 #c20)

* Sun Jul 05 2009 Robert Scheck <robert@fedoraproject.org> 1.2.2-1
- Upgrade to 1.2.2

* Sun May 10 2009 Robert Scheck <robert@fedoraproject.org> 1.2.1-2
- Re-added the forgotten MAPI_SERVER definement for Zarafa
- Enabled the allow_call_time_pass_reference in PHP settings
- Corrected STATE_DIR value from absolute to relative path

* Thu Apr 30 2009 Robert Scheck <robert@fedoraproject.org> 1.2.1-1
- Upgrade to 1.2.1
- Initial spec file for Fedora and Red Hat Enterprise Linux
