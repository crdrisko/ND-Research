// Name: functionptr-init.hpp - Version 1.0.0
// Author: cdrisko
// Date: 07/27/2020-15:01:08
// Description: Using the FunctionPtr initializer to create instances of SpecificFunctorBridge<>'s (C++14 and on)

#ifndef FUNCTIONPTR_INIT_HPP
#define FUNCTIONPTR_INIT_HPP

#include <type_traits>
#include <utility>

#include "functionptr.hpp"
#include "specificfunctorbridge.hpp"

template <typename R, typename... Args>
template <typename F>
FunctionPtr<R(Args...)>::FunctionPtr(F&& f) : bridge(nullptr)
{
    using Functor = std::decay_t<F>;
    using Bridge = SpecificFunctorBridge<Functor, R, Args...>;
    bridge = new Bridge(std::forward<F>(f));
}

#endif
