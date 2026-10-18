<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/hero-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/hero-light.svg">
    <img src="./assets/hero-light.svg" width="100%" alt="Xwift is the universal toolchain, built on its own fork of Swift. Write once. Run everything. Planned for macOS, Windows, Linux, Android, iOS and the web.">
  </picture>
</p>

<p align="center">
  <a href="#overview">Overview</a> &nbsp;·&nbsp;
  <a href="#projects">Projects</a> &nbsp;·&nbsp;
  <a href="#status">Status</a> &nbsp;·&nbsp;
  <a href="#contact">Contact</a>
</p>

<a id="overview"></a>
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/intro-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/intro-light.svg">
    <img src="./assets/intro-light.svg" width="100%" alt="Xwift is built to be the one toolchain you reach for on every platform you ship to. Write apps, tools and services in Swift, and Xwift compiles them to native code for macOS, Windows, Linux, Android, iOS and the web.">
  </picture>
</p>

<a id="universal"></a>
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/callout-universal-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/callout-universal-light.svg">
    <img src="./assets/callout-universal-light.svg" width="100%" alt="Universal. One codebase. Every platform.">
  </picture>
</p>

Xwift compiles one Swift codebase for desktop, mobile and the web. The proof of concept already builds, tests and runs on macOS, Linux, Windows and WebAssembly in CI. Android and iOS come next.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/code-universal-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/code-universal-light.svg">
    <img src="./assets/code-universal-light.svg" width="100%" alt="$ swift build
$ swift test
$ swift run xwift-hello
Hello from Xwift on linux-x86_64 (64-bit)!">
  </picture>
</p>

<a id="native"></a>
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/callout-native-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/callout-native-light.svg">
    <img src="./assets/callout-native-light.svg" width="100%" alt="Native. Real binaries on every target.">
  </picture>
</p>

Xwift compiles straight to native code through LLVM. No virtual machine and no bridge sit between your code and the platform. What you ship is a plain native binary.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/code-native-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/code-native-light.svg">
    <img src="./assets/code-native-light.svg" width="100%" alt="// From XwiftCore: resolved at compile time, once per target
private static var currentOS: OperatingSystem {
    #if os(macOS)
    return .macOS
    #elseif os(iOS)
    return .iOS
    #elseif os(Android)
    return .android
    #elseif os(Linux)
    return .linux
    #elseif os(Windows)
    return .windows
    #elseif os(WASI)
    return .wasi
    #else
    return .unknown
    #endif
}">
  </picture>
</p>

<a id="owned"></a>
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/callout-owned-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/callout-owned-light.svg">
    <img src="./assets/callout-owned-light.svg" width="100%" alt="Owned. Our fork. Our release cycle.">
  </picture>
</p>

Xwift keeps its own fork of the Swift compiler, driver, package manager and installer scripts. Today the fork matches Swift 6.4.1 with no patches. Every other dependency is pinned to an exact commit, so each build can be reproduced.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/code-owned-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/code-owned-light.svg">
    <img src="./assets/code-owned-light.svg" width="100%" alt="{
  &quot;_scheme&quot;: {&quot;name&quot;: &quot;xwift/0.1&quot;, &quot;aliases&quot;: [&quot;xwift/0.1&quot;]},
  &quot;swift&quot;:                   {&quot;repo&quot;: &quot;xwift-org/swift&quot;,                   &quot;branch&quot;: &quot;xwift/main&quot;},
  &quot;swift-driver&quot;:            {&quot;repo&quot;: &quot;xwift-org/swift-driver&quot;,            &quot;branch&quot;: &quot;xwift/main&quot;},
  &quot;swiftpm&quot;:                 {&quot;repo&quot;: &quot;xwift-org/swift-package-manager&quot;,   &quot;branch&quot;: &quot;xwift/main&quot;},
  &quot;swift-installer-scripts&quot;: {&quot;repo&quot;: &quot;xwift-org/swift-installer-scripts&quot;, &quot;branch&quot;: &quot;xwift/main&quot;}
}">
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/swoop-1-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/swoop-1-light.svg">
    <img src="./assets/swoop-1-light.svg" width="100%" alt="">
  </picture>
</p>

<a id="familiar"></a>
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/callout-familiar-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/callout-familiar-light.svg">
    <img src="./assets/callout-familiar-light.svg" width="100%" alt="Familiar. It is Swift. Keep what you know.">
  </picture>
</p>

Xwift speaks the Swift language and SwiftPM. Packages, tests and skills carry over unchanged, and the fork is synced from upstream Swift releases.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/code-familiar-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/code-familiar-light.svg">
    <img src="./assets/code-familiar-light.svg" width="100%" alt="// swift-tools-version:6.0
import PackageDescription

let package = Package(
    name: &quot;Xwift&quot;,
    products: [
        .library(name: &quot;XwiftCore&quot;, targets: [&quot;XwiftCore&quot;]),
        .executable(name: &quot;xwift-hello&quot;, targets: [&quot;xwift-hello&quot;]),
    ],
    targets: [
        .target(name: &quot;XwiftCore&quot;),
        .executableTarget(name: &quot;xwift-hello&quot;, dependencies: [&quot;XwiftCore&quot;]),
        .testTarget(name: &quot;XwiftCoreTests&quot;, dependencies: [&quot;XwiftCore&quot;]),
    ],
    swiftLanguageModes: [.v6]
)">
  </picture>
</p>

<a id="projects"></a>
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/callout-projects-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/callout-projects-light.svg">
    <img src="./assets/callout-projects-light.svg" width="100%" alt="Complete. One stack, top to bottom.">
  </picture>
</p>

The toolchain comes first. A UI framework, system APIs and a package manager follow, each in its own repository.

- **Toolchain.** The compiler, driver and package manager, forked from Swift 6.4.1. Private, in Phase 0.
- **UI framework.** One declarative UI for every target. Planned.
- **System APIs.** Files, networking, processes and devices, the same everywhere. Planned.
- **Package manager.** Packages and a registry for all six targets. Planned.

<a id="status"></a>
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/section-status-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/section-status-light.svg">
    <img src="./assets/section-status-light.svg" width="100%" alt="Status. Early, and clear about it.">
  </picture>
</p>

- **Phase 0 is done.** Private mirrors of the Swift compiler, driver, package manager and installer scripts, plus a reproducible build setup.
- **The proof of concept runs.** One package builds, tests and runs on macOS, Linux, Windows and WebAssembly in CI.
- **Not released.** There is no public toolchain, no website and no download yet. The source repositories are private.
- **License.** Not chosen yet.

<a id="contact"></a>
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/section-contact-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/section-contact-light.svg">
    <img src="./assets/section-contact-light.svg" width="100%" alt="Contact. Questions, ideas, early interest.">
  </picture>
</p>

Write to [vido.teodor10@gmail.com](mailto:vido.teodor10@gmail.com). Watch [xwift-org](https://github.com/xwift-org) for the first public repositories.

<p align="center">
  <a href="mailto:vido.teodor10@gmail.com"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/closing-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/closing-light.svg">
    <img src="./assets/closing-light.svg" width="100%" alt="Follow Along. Xwift is early. This is the time to join. vido.teodor10@gmail.com · github.com/xwift-org">
  </picture></a>
</p>

<sub>Xwift is an independent project. It is not affiliated with or endorsed by Apple Inc. Swift is a trademark of Apple Inc.</sub>
