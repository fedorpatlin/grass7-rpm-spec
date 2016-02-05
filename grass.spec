#
# spec file for package grass
#
# Copyright (c) 2015 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%define	shortver 70

Name:		grass7
Version:	7.0.3
Release:	1%{?dist}
License:	GPLv2+
Summary:	GRASS - Geographic Resources Analysis Support System
URL:		http://grass.osgeo.org
Group:		Applications/Engineering
Source0:	http://grass.osgeo.org/grass%{shortversion}/source/grass-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       gdal >= 1.11.0
Requires:       proj >= 4.7.0
Requires:       sqlite >= 3
Requires:       unixODBC
Requires:       xterm
Requires:       fftw
Requires:       geos >= 3
Requires:       netcdf
Requires:       python >= 2.6
Requires:       wxPython >= 2.8

BuildRequires: rpm-build
BuildRequires: make
BuildRequires: tar
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: bison
BuildRequires: flex
BuildRequires: freetype-devel
BuildRequires: gcc-c++
BuildRequires: geos-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: man
BuildRequires: proj
BuildRequires: netcdf-devel
BuildRequires: proj-devel
BuildRequires: libtiff-devel
BuildRequires: mysql-devel
BuildRequires: ncurses-devel
BuildRequires: postgresql-devel
BuildRequires: sqlite-devel
BuildRequires: unixODBC-devel
BuildRequires: zlib-devel
BuildRequires: fftw-devel
BuildRequires: fftw3-devel
BuildRequires: fdupes
BuildRequires: libXmu-devel
BuildRequires: numpy
BuildRequires: perl
BuildRequires: python-devel
BuildRequires: python-opengl
BuildRequires: wxPython-devel
BuildRequires: python-dateutil
BuildRequires: wxWidgets-devel
BuildRequires: readline-devel
BuildRequires: mysql-devel
BuildRequires: blas-devel
BuildRequires: lapack-devel
BuildRequires: gettext


%package docs
Summary:        Documentation for GRASS GIS 7
Group:          Applications/Engineering
Requires:       %{name} = %{version}

%package devel
Summary:        Development files for GRASS GIS 7
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description
GRASS (Geographic Resources Analysis Support System), commonly
referred to as GRASS, is a Geographic Information System
(GIS) used for geospatial data management and analysis, image
processing, graphics/maps production, spatial modeling, and
visualization. GRASS is currently used in academic and commercial
settings around the world, as well as by many governmental agencies
and environmental consulting companies.

%description devel
This package contains the development files for GRASS GIS

%description docs
This package contains the HTML documentation files for GRASS GIS

%clean
%prep
%setup -q -n grass-%{version}
%define grasver -@GRASS_VERSION_MAJOR@.@GRASS_VERSION_MINOR@.@GRASS_VERSION_RELEASE@
%define grasver2 '-${GRASS_VERSION_MAJOR}.${GRASS_VERSION_MINOR}.${GRASS_VERSION_RELEASE}'

sed -i s/%{grasver}//g include/Make/Platform.make.in
sed -i s/%{grasver}//g grass.pc.in
sed -i s/%{grasver2}//g configure
sed -i s/%{grasver2}//g Makefile
sed -i 's:STARTUP = $(UNIX_BIN)/$(GRASS_NAME):STARTUP = $(DESTDIR)/$(UNIX_BIN)/$(GRASS_NAME):g' include/Make/Install.make

# Setup symlink grassgis70 to relative path
sed -i 's|ln -sf $BINDIR/grass-$NAME_VER $BINDIR/$GRASSPRG|pushd $BINDIR; ln -sf grass-$NAME_VER $GRASSPRG; popd|' binaryInstall.src

%define grassdir /opt/grass7
%define grasslib %{grassdir}/lib

#configure with shared libs:
%configure \
	--enable-largefile \
	--enable-shared \
	--with-blas \
	--with-cairo \
	--with-cxx \
	--with-fftw \
	--with-freetype-includes=/usr/include/freetype2\
	--with-freetype=yes \
	--with-gdal \
	--with-geos \
	--with-glw \
	--with-lapack \
	--with-motif \
	--with-mysql \
	--with-mysql-includes=/usr/include/mysql \
	--with-mysql-libs=/usr/lib64/mysql \
	--with-nls \
	--with-netcdf\
	--with-odbc \
	--with-opengl \
	--with-openmp\
	--with-postgres  \
	--with-proj \
	--with-pthread\
	--with-python \
	--with-readline \
	--with-sqlite \
	--with-wxwidgets=wx-config \
	--with-x\


%build
make

%install
cp -rfv locale dist.*

# Installing with script included in GRASS distribution
# Set BINDISTNAME to easy install
sed -i 's+BINDISTNAME = grass-$(GRASS_VERSION_NUMBER)-$(ARCH)-$(DATE)+BINDISTNAME = grass+' include/Make/Install.make
make bindist 
./grass-install.sh grass.tar.gz %{buildroot}%{grassdir} %{buildroot}%{grassdir}

# Removing BUILDROOT from installed scripts 
sed -i "s:%{buildroot}::" %{buildroot}%{grassdir}%{_sysconfdir}/fontcap
sed -i "s:%{buildroot}::" %{buildroot}%{grassdir}/grass-%{version}-*
sed -i "s:%{buildroot}::" %{buildroot}%{grassdir}/include/Make/Platform.make

# make grass libraries available on the system
install -d %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo %{grasslib} >> %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{version}.conf

# also make grass executables available
install -d %{buildroot}%{_sysconfdir}/profile.d
echo 'export PATH=$PATH:%{grassdir}' > %{buildroot}%{_sysconfdir}/profile.d/%{name}-%{version}.sh
echo 'setenv PATH $PATH:%{grassdir}' > %{buildroot}%{_sysconfdir}/profile.d/%{name}-%{version}.csh

%fdupes -s %{buildroot}%{grassdir}

%files devel
%defattr(-,root,root)
%{grassdir}/include
%{grasslib}/*.a
%{grassdir}/locale/po/*
%{grassdir}/locale/scriptstrings/*
%{grassdir}/locale/templates/*
%{grassdir}/locale/Makefile
%{grassdir}/locale/README
%{grassdir}/locale/grass_po_stats.*

%files docs
%defattr(-,root,root)
%{grassdir}/docs/html/*
%{grassdir}/docs/man/*

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/%{name}-%{version}.*
%{_sysconfdir}/ld.so.conf.d/%{name}-%{version}.conf
%{grassdir}/bin/*
%{grassdir}%{_sysconfdir}*
%{grassdir}/gui/*
%{grassdir}/scripts/*
%{grassdir}/share/applications/grass.desktop
%{grassdir}/share/appdata/grass.appdata.xml
#%{grassdir}/bwidget/*
%lang(ar) %{grassdir}/locale/ar/LC_MESSAGES/*.mo
%lang(cs) %{grassdir}/locale/cs/LC_MESSAGES/*.mo
%lang(de) %{grassdir}/locale/de/LC_MESSAGES/*.mo
%lang(el) %{grassdir}/locale/el/LC_MESSAGES/*.mo
%lang(es) %{grassdir}/locale/es/LC_MESSAGES/*.mo
%lang(fr) %{grassdir}/locale/fr/LC_MESSAGES/*.mo
%lang(fi) %{grassdir}/locale/fi/LC_MESSAGES/*.mo
#%lang(hi) %{grassdir}/locale/hi/LC_MESSAGES/*.mo
%lang(id) %{grassdir}/locale/id/LC_MESSAGES/*.mo
%lang(it) %{grassdir}/locale/it/LC_MESSAGES/*.mo
%lang(ja) %{grassdir}/locale/ja/LC_MESSAGES/*.mo
%lang(ko) %{grassdir}/locale/ko/LC_MESSAGES/*.mo
%lang(lv) %{grassdir}/locale/lv/LC_MESSAGES/*.mo
%lang(ml) %{grassdir}/locale/ml/LC_MESSAGES/*.mo
#%lang(mr) %{grassdir}/locale/mr/LC_MESSAGES/*.mo
%lang(pl) %{grassdir}/locale/pl/LC_MESSAGES/*.mo
%lang(pt) %{grassdir}/locale/pt/LC_MESSAGES/*.mo
%lang(pt_br) %{grassdir}/locale/pt_br/LC_MESSAGES/*.mo
%lang(ru) %{grassdir}/locale/ru/LC_MESSAGES/*.mo
%lang(ro) %{grassdir}/locale/ro/LC_MESSAGES/*.mo
%lang(sl) %{grassdir}/locale/sl/LC_MESSAGES/*.mo
%lang(th) %{grassdir}/locale/th/LC_MESSAGES/*.mo
%lang(tr) %{grassdir}/locale/tr/LC_MESSAGES/*.mo
%lang(vi) %{grassdir}/locale/vi/LC_MESSAGES/*.mo
%lang(zh) %{grassdir}/locale/zh/LC_MESSAGES/*.mo
%{grassdir}/tools/*.py*
%{grassdir}/tools/g.echo
%{grassdir}/driver/*
%{grassdir}/fonts/*
%{grasslib}/*.so
#%{grassdir}/config.status
%{grassdir}/AUTHORS
%{grassdir}/translators.csv
#%{grassdir}/translation_status.json
%{grassdir}/contributors*
%{grassdir}/CHANGES
%{grassdir}/COPYING
%{grassdir}/GPL.TXT
%{grassdir}/REQUIREMENTS.html
%{grassdir}/share/icons/*
%{grassdir}/grass*
%exclude %{grassdir}/demolocation
%exclude %{grassdir}/grass70.tmp
%defattr(755,root,root)

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog

