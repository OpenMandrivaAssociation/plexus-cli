%{?_javapackages_macros:%_javapackages_macros}

%global parent plexus
%global subname cli

Name:           %{parent}-%{subname}
Version:        1.6
Release:        2.3
Epoch:          0
Summary:        Command Line Interface facilitator for Plexus
Group:		Development/Java
License:        ASL 2.0

URL:            https://plexus.codehaus.org/
# git clone git://github.com/codehaus-plexus/plexus-cli.git
# git --git-dir plexus-cli/.git archive --prefix plexus-cli-1.6/ 8927458e81 | xz >plexus-cli-1.6.tar.xz
Source0:        %{name}-%{version}.tar.xz
Source1:        LICENSE-2.0.txt

# License headers missing from some files
# http://jira.codehaus.org/browse/PLX-418
Patch0:         plexus-cli-licenseheaders.patch

BuildArch:      noarch

BuildRequires:	junit
BuildRequires:  maven-local
BuildRequires:  mvn(commons-cli:commons-cli)
BuildRequires:  mvn(org.codehaus.plexus:plexus-components:pom:)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)

%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.

%package javadoc
Summary:        Javadoc for %{name}

Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q

cp -p %{SOURCE1} .

%mvn_file : plexus/cli

%pom_add_dep junit:junit::test

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE-2.0.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE-2.0.txt

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Mat Booth <fedora@matbooth.co.uk> - 0:1.2-17
- Remove unneeded BRs, rhbz #915617

* Thu Feb 28 2013 Mat Booth <fedora@matbooth.co.uk> - 0:1.2-16
- Include a copy of the licence, rhbz #880282

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.2-14
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Nov 16 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2-13
- Fix license tag to be ASL 2.0 (no plexus licensing anywhere)
- Update to new guidelines

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 12 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.2-10
- Build with maven 3.x

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 21 2009 Andrew Overholt <overholt@redhat.com> 0:1.2-8
- Add jakarta-commons-cli BR

* Thu Aug 20 2009 Andrew Overholt <overholt@redhat.com> 0:1.2-7
- Remove gcj support
- Default to building with ant
- Add patch to include fixed file headers
  (http://jira.codehaus.org/browse/PLX-418)

* Sun May 17 2009 Fernando Nasser <fnasser@redhat.com> 0:1.2-6
- Fix license and source URL

* Tue Apr 30 2009 Yong Yang <yyang@redhat.com> 0:1.2-5
- Add BRs maven-doxia*
- Rebuild with new maven2 2.0.8 built in non-bootstrap mode

* Tue Mar 17 2009 Yong Yang <yyang@redhat.com> 0:1.2-4
- rebuild with new maven2 2.0.8 built in bootstrap mode

* Thu Feb 05 2009 Yong Yang <yyang@redhat.com> 0:1.2-3
- fix release tag

* Wed Jan 14 2009 Yong Yang <yyang@redhat.com> 0:1.2-2jpp.2
-re-build with gcj

* Wed Jan 14 2009 Yong Yang <yyang@redhat.com> 0:1.2-2jpp.1
- Import from maven 2.0.8 packages, initial bulding

* Wed Jan 30 2008 Deepak Bhole <dbhole@redhat.com> 0:1.2-1jpp.1
- Initial build with merge from JPackage
