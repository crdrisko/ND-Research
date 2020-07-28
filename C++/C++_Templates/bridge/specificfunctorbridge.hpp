// Name: specificfunctorbridge.hpp - Version 1.0.0
// Author: cdrisko
// Date: 07/27/2020-15:01:00
// Description: Definition of the derived class for our FunctorBridge

#ifndef SPECIFICFUNCTORBRIDGE_HPP
#define SPECIFICFUNCTORBRIDGE_HPP

#include <utility>

#include "functorbridge.hpp"

template <typename Functor, typename R, typename... Args>
class SpecificFunctorBridge : public FunctorBridge<R, Args...>
{
private:
    Functor functor;

public:
    template <typename FunctorFwd>
    SpecificFunctorBridge(FunctorFwd&& functor) : functor(std::forward<FunctorFwd>(functor)) {}

    virtual SpecificFunctorBridge* clone() const override { return new SpecificFunctorBridge(functor); }
    virtual R invoke(Args... args) const override { return functor(std::forward<Args>(args)...); }
};

#endif
