Summary: Lua script engine module for nginx
Name: nginx-mod-lua
Version: 0.10.15
Release: 1%{?dist}
Vendor: Artera
URL: https://github.com/openresty/lua-nginx-module

%define _modname            lua
%define _nginxver           1.16.1
%define nginx_config_dir    %{_sysconfdir}/nginx
%define nginx_build_dir     %{_builddir}/nginx-%{_nginxver}

Source0: https://nginx.org/download/nginx-%{_nginxver}.tar.gz
Source1: https://github.com/openresty/lua-nginx-module/archive/v%{version}/%{_modname}-%{version}.tar.gz

Requires: nginx = 1:%{_nginxver}
Requires: nginx-mod-ndk-set-misc
Requires: luajit
BuildRequires: nginx
BuildRequires: luajit-devel
BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: zlib-devel
BuildRequires: perl-devel
BuildRequires: gd-devel
BuildRequires: GeoIP-devel
BuildRequires: libxslt-devel
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: gperftools-devel

License: BSD

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Lua script engine module for nginx.

%prep
%setup -q -n nginx-%{_nginxver}
%setup -T -D -b 1 -n %{_modname}-nginx-module-%{version}

%build
cd %{_builddir}/nginx-%{_nginxver}
./configure %(nginx -V 2>&1 | grep 'configure arguments' | sed -r 's@^[^:]+: @@') --add-dynamic-module=../%{_modname}-nginx-module-%{version}
make modules

%install
%{__rm} -rf %{buildroot}

%{__install} -Dm755 %{nginx_build_dir}/objs/ngx_http_lua_module.so \
    $RPM_BUILD_ROOT%{_libdir}/nginx/modules/ngx_http_lua_module.so

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/nginx/modules/*.so
