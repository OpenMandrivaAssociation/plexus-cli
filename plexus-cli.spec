# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define with_maven 0

%define parent plexus
%define subname cli
%define namedversion 1.2

Name:           %{parent}-%{subname}
Version:        1.2
Release:        11
Summary:        Command Line Interface facilitator for Plexus
License:        ASL 2.0 and Plexus
Group:          Development/Java
URL:            http://plexus.codehaus.org/
# svn export http://svn.codehaus.org/plexus/archive/plexus-tools/tags/plexus-cli-1.2
# tar czf plexus-cli-%{version}-src.tar.gz plexus-cli-%{version}
# Note: Exported revision 8188.
Source0:        %{name}-%{namedversion}-src.tar.gz

Source1:        plexus-cli-1.2-build.xml
Source2:        plexus-cli-settings.xml
Source3:        plexus-cli-1.2-jpp-depmap.xml

# License headers missing from some files
# http://jira.codehaus.org/browse/PLX-418
Patch0:         plexus-cli-licenseheaders.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  jpackage-utils >= 0:1.7.3
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  junit
%if %{with_maven}
BuildRequires:  maven2 >= 2.0.4-10jpp
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-surefire = 2.3
BuildRequires:  maven-surefire-provider-junit = 2.3
BuildRequires:  maven-doxia
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-release
%endif
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-utils 
BuildRequires:  jakarta-commons-cli
BuildRequires:	guava

Requires:  plexus-classworlds
Requires:  plexus-containers-container-default
Requires:  plexus-utils 
Requires(post):    jpackage-utils >= 0:1.7.3
Requires(postun):  jpackage-utils >= 0:1.7.3

%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}
find . -name "*.jar" -exec rm -f {} \;
#for j in $(find . -name "*.jar" ); do
#        mv $j $j.no
#done

%patch0 -p3

cp %{SOURCE1} build.xml
cp %{SOURCE2} settings.xml

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

%if %{with_maven}
mvn-jpp \
        -e \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven2.jpp.depmap.file=%{SOURCE3} \
        install javadoc:javadoc

%else
export CLASSPATH=$(build-classpath \
plexus/classworlds \
plexus/containers-container-default \
plexus/utils  \
commons-cli \
guava \
)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes

ant -Dbuild.sysclasspath=only jar javadoc
%endif


%install

# jars
install -d -m 755 %{buildroot}%{_javadir}/plexus
install -pm 644 target/%{name}-%{namedversion}.jar \
 	%{buildroot}%{_javadir}/plexus/%{subname}-%{version}.jar
%add_to_maven_depmap org.codehaus.plexus %{name} %{namedversion} JPP/%{parent} %{subname}

(cd %{buildroot}%{_javadir}/%{parent} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# pom
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -pm 644 pom.xml %{buildroot}%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}.pom

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%clean
rm -rf %{buildroot}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_javadir}/%{parent}/*
%{_datadir}/maven2
%{_mavendepmapfragdir}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/*


