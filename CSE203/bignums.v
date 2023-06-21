(* --------------------------------------------------------------------- *)
From mathcomp Require Import all_ssreflect all_algebra.

Set   Implicit Arguments.
Unset Strict Implicit.
Unset Printing Implicit Defensive.

Set Printing Coercions.

(* --------------------------------------------------------------------- *)
(* The goal of this project is to develop a minimal library for          *)
(* arbitrary-precision arithmetic, also called bignums.                  *)
(*                                                                       *)
(* Arbitrary-precision arithmetic refers to the set of techniques used   *)
(* to manipulate numbers (mainly integers or rational) of arbitrary size *)
(* in a computer program. Arbitraty-precision arithmetic is opposed      *)
(* fixed-precision arithmetic (found in most arithmetic logic unit       *)
(* (ALU) hardware) and that deals only with 32 or 64 bit numbers.        *)
(*                                                                       *)
(* Several modern programming languages have built-in support for        *)
(* bignums (e.g. Python or Coq with the type `nat`), and various         *)
(* libraries provide efficient data structures and operations for        *)
(* arbitrary-precision computing.                                        *)
(*                                                                       *)
(* In most bignum libraries, rather than storing values as a fixed       *)
(* number of bits related to the size of the processor register, they    *)
(* typically use a variable-length arrays of machine words.              *)
(*                                                                       *)
(* For example, on a 32-bit machine, one (unsigned) machine word can     *)
(* store integers from 0 to 2^32 (excluded). If we want to store an      *)
(* integer greater or equal than 2^32, we have to use at least two       *)
(* machine words. For example, if we use exactly two machine words       *)
(* w0 & w1, we have then 64 bits at our disposal and can therefore       *)
(* store integers from 0 to 2^64 (excluded).                             *)
(*                                                                       *)
(* One way to do this is to use a base 2^32 numbering system where `w0`  *)
(* is the units digit and `w1` the tens digit. Thus, the pair of machine *)
(* words `(w0, w1)` represents the number `w0 + 2^32 * w1`.              *)
(*                                                                       *)
(* If we need to store a number larger or equal than `2^64`, we can use  *)
(* a third digit `w2`. In this case, `w2` plays the role of the hundreds *)
(* digit and the triplet (w0, w1, w2) represents the integer             *)
(* `w0 + 2^32 * w1 + 2^(2*32) * w2`. Using three words, we can then      *)
(* represent numbers up to 2^96 (excluded).                              *)
(*                                                                       *)
(* In the case of a bignum library, to represent integers, we use a      *)
(* variable-length array (or list) of machine words. Such a list `ws`    *)
(* represents the integer:                                               *)
(*                                                                       *)
(*    \sum_(0 <= i < |ws|) 2^(i*32) * ws_i                               *)
(*                                                                       *)
(* where `|ws|` is the length of the list `ws` and `ws_i` is the i-th    *)
(* element of `ws`.                                                      *)

(* --------------------------------------------------------------------- *)
(* In this project, to represent bignum, we will use lists of machine    *)
(* words of size `(8 * size)`, where `size` is some positive natural     *)
(* number that represents the size (in bytes) of the hardware            *)
(* machine-word:                                                         *)

Context
  (size     :  nat)
  (gt0_size :  (0 < size)%N)
  (wsize    := 2 ^ (8 * size))
  (word     := 'Z_wsize)
  (bignum   := seq word).

(* -------------------------------------------------------------------- *)
(* We provide some basic results on `wsize`                             *)

Lemma gt1_wsize : 1 < wsize.
Proof.
rewrite /wsize -{1}[1](expn0 2) ltn_exp2l // lt0n.
by rewrite muln_eq0 /= -lt0n gt0_size.
Qed.

Hint Extern 0 (is_true (1 < wsize)) => exact: gt1_wsize : core.

Lemma gt0_wsize : 0 < wsize.
Proof. by apply: (@leq_trans 2). Qed.

Hint Extern 0 (is_true (0 < wsize)) => exact: gt0_wsize : core.

(* Here, 'Z_p is the type of integers modulo `p` that provides a good    *)
(* absraction of what a machine word is. You can use the standard ring   *)
(* operations on values of type 'Z_p.                                    *)

(* Note: the command above is equivalent to:                             *)
(*                                                                       *)
(*   Parameter  (size : nat).                                            *)
(*   Hypothesis (gt0_size : (0 < size)%N)                                *)
(*                                                                       *)
(*   Definition wsize  := 2 ^ (8 * size).                                *)
(*   Definition word   := 'Z_wsize.                                      *)
(*   Definition bignum := seq word.                                      *)

(* --------------------------------------------------------------------- *)
(* In this project, you might want to convert values between natural     *)
(* numbers and words. For that purpose, you can use the `toword` and     *)
(* nat_of_ord operators:                                                 *)

Notation toword n := (inord n : word) (only parsing).

Lemma towordK (n : nat) : n < wsize -> nat_of_ord (toword n) = n.
Proof.
by move=> le; rewrite inordK // !prednK // ltn_predRL.
Qed.

Lemma ofwordK (w : word) : toword (nat_of_ord w) = w.
Proof. by rewrite inord_val. Qed.

Lemma ltn_nat_of_ord (w : word) : nat_of_ord w < wsize.
Proof. by case: w => /= w; rewrite !prednK // ltn_predRL. Qed.

(* --------------------------------------------------------------------- *)
(* In the course of this project, you might want to use the following    *)
(* lemmas about natural integer arithmetic:                              *)
(*                                                                       *)
(*   addn0, add0n, addnC, addnA                                          *)
(*   muln0, mul0n, mulnC, mulnA                                          *)
(*   muln1, mul1n, mulnS                                                 *)
(*                                                                       *)
(* You can do a `Check lemma_name` do this what `lemma_name` proves.     *)
(*                                                                       *)
(* As a general note, if you are stuck because you are missing some      *)
(* basic properties about natural numbers, just put it as an axiom and   *)
(* go forward.                                                           *)


(* ===================================================================== *)
(* Changing the representation (nat <-> bignum)                          *)
(* ===================================================================== *)

(* In this first part, we will write the conversion functions between    *)
(* the natural numbers (the values of type `nat`) and the type           *)
(* `bignum`, as well as proving different results about them. These      *)
(* functions will allow us later to state the correctness lemmas of      *)
(* the implementations of the arithmetic operations.                     *)

(* 1. Implement the function `bn2nat` s.t. `bn2nat z` returns the        *)
(*    natural number represented by the bignum `z`, i.e.                 *)
(*                                                                       *)
(*    bn2nat z := z_0 + z_1 * 2^32 + z_2 * 2^64 + ... + 2_n * 2^(n*32)   *)
(*                                                                       *)
(* Values of type 'Z_p are automatically converted to `nat` when needed. *)
(* However, you can force the conversion using the function              *)
(* `nat of ord`.                                                         *)
(*                                                                       *)
(* (In all the question asking you to define a fuction, you are free to  *)
(* change `Definition` to `Fixpoint` if needed).                         *)

Fixpoint bn2nat (bn : bignum) : nat :=
match bn with
| nil => 0
| cons x y => x + wsize * (bn2nat y)
end.

(* 2. Implement the function `nat2bn` s.t. `nat2bn n` computes the       *)
(*    bignum that represents the natural number `n`.                     *)
(*                                                                       *)
(* In this function, you can use the following operations:               *)
(*                                                                       *)
(*   - n %% p : computes `n` modulo `p` for `(n p : nat)`                *)
(*   - n %/ p : computes the quotient of the division of `n` by `p`      *)
(*                                                                       *)

(* In this lemma, you might want to use `divn_eq`                        *)
(*                                                                       *)
(*   divn_eq                                                             *)
(*     : forall m d : nat, m = m %/ d * d + m %% d                       *)
(*                                                                       *)
(* We also provide the following lemma:                                  *)

Lemma nat2bn_help1 n p : n < p.+1 -> n.+1 %/ wsize <= p.
Proof.
move/leq_div2r => /(_ wsize) /leq_trans; apply.
case: p => [|p]; first rewrite divn_small //.
have := leq_divDl wsize p.+1 1; rewrite addn1.
move/leq_trans; apply; rewrite [1%/_]divn_small //.
rewrite addn0 addn1; apply: ltn_Pdiv => //.
Qed.

(* recursively convert num into bignum list until nil *)

Fixpoint nat2ban_Helper (n : nat) (m : nat) : bignum :=
match m with
| 0 => [::]
| S m' => 
    (match n with
    | 0 => [::]
    | S y => inord (n %% wsize) :: (nat2ban_Helper (n %/ wsize) m')
    end)
end.

Definition nat2bn (n : nat) : bignum :=
  nat2ban_Helper n n.

(* Test the function :=
      Eval compute in (nat2bn 5). *)

(* 3. Prove that `nat2bn` and `bn2nat` are self-invert.                  *)
(*                                                                       *)
(*    Such a result is sufficient to prove that you have a               *)
(*    correct & complete representation of arbitrary-precision           *)
(*    numbers:                                                           *)
(*                                                                       *)
(*      - you can represent any natural number using a bignum, and       *)
(*      - two different bignums never represent the same number.         *)
(*                                                                       *)

(* elim gives me inductive hypotheses to work with as assumptions I think*)
(* this makes code compact and life much easier                          *)

Lemma nat2bnK_Helper : forall (n m : nat), m <= n -> bn2nat (nat2ban_Helper m n) = m.
Proof.
elim => [| n IHn] //=.
  by move => m; case m.

  elim => [| m IHm].
    done.

(* I need to apply IHn so I need other hypotheses that can help me get it *)
(* I use H1 and H2 to apply IHn and rewrite my subgoal                    *)
  move => H1 //=.
  move: (nat2bn_help1 H1) => H2.
  rewrite (IHn (m.+1 %/ wsize) H2).
  rewrite towordK.
(* I need to conver the subgoal into right form to use divn_eq            *)
  rewrite mulnC // addnC.
  by rewrite -(divn_eq (m.+1) wsize).
(*  Search(_%%_<_). *)
  by apply (ltn_pmod).
Qed.

(* I need a helper function so that I can use the nat2bn function         *)
(* The statement of my nat2bnK_Helper function only makes sense because   *)
(* m <= n is a critical idea for that function hence I prove the lemma    *)

Lemma nat2bnK : cancel nat2bn bn2nat.
Proof.
by move => n; apply nat2bnK_Helper.
Qed.

(* --------------------------------------------------------------------- *)
(* !! OPTIONAL                                                           *)

Definition canon (z : bignum) :=
  if rev z is x :: _ then x != 0%R else true.

Lemma bn2natK (z : bignum) :
  canon z -> nat2bn (bn2nat z) = z.
Proof. Admitted.

(* ===================================================================== *)
(* Addition of bignums                                                   *)
(* ===================================================================== *)

(* We are now interested in adding bignums: given `z1 z2 : bignum`, we   *)
(* want to compute a bignum `bnadd z1 z2` s.t.                           *)
(*                                                                       *)
(*   bn2nat z = bn2nat z1 + b2nat z2                                     *)
(*                                                                       *)
(* Of course, one could directly use the arithmetical operations of      *)
(* `nat` to implement `bn2nat`, i.e.                                     *)
(*                                                                       *)
(*   Definition bn2nat (z1 z2 : bignum) : bignum :=                      *)
(*     bn2nat (nat2bn z1 + nat2bn z2).                                   *)
(*                                                                       *)
(* However, using a bignum library to implement a bignum library would   *)
(* totally defeat the purpose of this project. AS SUCH, IN ALL THIS      *)
(* PROJECT, IT IS STRICTLY FORBIDDEN TO USE THE ARTIHMTIC OF NAT TO      *)
(* IMPLEMENT THE BIGNUM OPERATIONS.                                      *)

(* Instead, we need to come with a way to implement them by only         *)
(* resorting on the machine word arithmetic operations. For addition,    *)
(* the best algorithm is simply the school-book addition that you all    *)
(* learnt in elementary school (here given in pseudo-code):              *)
(*                                                                       *)
(*   proc bnadd(z1 : bignum, z2 : bignum) : bignum {                     *)
(*     n : nat    <- max (size z1, size z2)                              *)
(*     z : bignum <- [::]                                                *)
(*     c : carry  <- false                                               *)
(*                                                                       *)
(*     for i = 0 to n-1 {                                                *)
(*       c, w <- word_add_with_carry(z1_i, z2_i, c)                      *)
(*       z    <- z ++ [:: w]                                             *)
(*     }                                                                 *)
(*     if (c) {                                                          *)
(*       z <- z ++ [:: 1]                                                *)
(*     }                                                                 *)
(*     return z                                                          *)
(*   }                                                                   *)
(*                                                                       *)
(* where `word_add_with_carry(w1, w2, c)` returns a pair `(c2, w)`       *)
(* where `w` is the result of the addition of `w1 + w2 + c` (using       *)
(* modular arithmetic) and `c` is a carry flag (a boolean) that          *)
(* indicates wether an integer overflow occured. Also, to ease the       *)
(* presentation, note that we assumed that `z_i` is the machine word `0` *)
(* when `i` is out of bounds.                                            *)
(*                                                                       *)
(* The operation `word_add_with carry` is something that is provided by  *)
(* the  ALU of the hardware, and we will assume given its                *)
(* implementation:                                                       *)

Context (word_add_with_carry : word -> word -> bool -> bool * word).

Axiom word_add_with_carry_correct :
  forall (w1 w2 : word) (c : bool),
    let: (c', w) := word_add_with_carry w1 w2 c in
    nat_of_ord w1 + nat_of_ord w2 + nat_of_bool c = w + (nat_of_bool c') * wsize.

(* 4. Implement the function `bnadd` that computes the addition of two   *)
(*    bignums, using the algorithm given above.                          *)

(*  copy the pseudo-code  *)

Fixpoint bnaddcarry (bn : bignum) (c: bool) :=
  match bn, c with
  | [::]  , true => [::inord (c)]
  | [::]  , false => [::]
  | elem::bn' , _ => 
            (let (c1, elem) := word_add_with_carry (inord 0) elem c 
             in
             elem::(bnaddcarry bn' c1))
end.

Fixpoint bnadd_Helper (bn1 bn2 : bignum) (c: bool): bignum :=
  match bn1 with
  | [::]    => bnaddcarry bn2 c
  | elem1::bn1' => 
          ( match bn2 with
            | [::]    => bnaddcarry bn1 c
            | elem2::bn2' => (let (c1, elem) := word_add_with_carry elem1 elem2 c 
                              in
                              elem::(bnadd_Helper bn1' bn2' c1))
           end)
end.

Definition bnadd (z1 z2 : bignum) : bignum :=
  bnadd_Helper z1 z2 false.

(* 5. Prove that `bnadd` is correct, as stated below.                    *)

Axiom mulcabA: forall (a b c : nat),
        c * ( a + b ) = (c * a) + (c * b).

Axiom boolmulA: forall (n : nat) (b : bool), 
        n * b = b * n.

Lemma bnaddcarry_correct: forall (bn: bignum) (c: bool),
  bn2nat (bnaddcarry bn c) = bn2nat bn + c.
Proof.
elim => [| elem bn IHbn] c //=.

  case one: c. simpl.
    rewrite towordK // muln0.
    reflexivity. done.

(* I don't need recursion here because a case-analysis will be sufficient *)
  case word: (word_add_with_carry (inord 0) elem c) => [c0 elem0] //=.
    rewrite (IHbn c0) //=.
(* I need to convert wsize * c0 into c                                    *)
    move : (word_add_with_carry_correct (inord 0) elem c).
    rewrite word.
    rewrite mulcabA.
    move => temp.
    rewrite boolmulA // (addnC (wsize * bn2nat bn)  (c0 * wsize)) // addnA.
    rewrite -temp.
    rewrite towordK //add0n // addnC // addnA (addnC (wsize * bn2nat bn) elem).
    trivial.
Qed.

Axiom addAn: forall (n m k: nat), 
        n + m + k = n + (m + k).

Lemma bnadd_correct_Helper: forall (bn1 bn2: bignum) (c: bool),
  bn2nat (bnadd_Helper bn1 bn2 c) = bn2nat bn1 + bn2nat bn2 + c.
Proof.
elim => [| w1 bn1 IHbn1].
  apply bnaddcarry_correct.

  elim => [| w2 bn2 IHbn2].
    move => c.
    by rewrite (bnaddcarry_correct (w1 :: bn1) c) //= // addn0.

    move => c //=.
    case h: (word_add_with_carry w1 w2 c) => [c1 elem] //=.
      rewrite IHbn1.
(* I need to rewrite w1 w2 c hence I use word_add_with_carry_correct      *)
      move: ( word_add_with_carry_correct w1 w2 c).
      rewrite h // !mulcabA.
      move => h1.
      rewrite addnA // boolmulA // (addnC elem (wsize * bn2nat bn1 + wsize * bn2nat bn2)).
      rewrite (addnC w2 (wsize * (bn2nat bn2))) // addnA.
      rewrite (addAn (wsize * bn2nat bn1 + wsize * bn2nat bn2) elem (c1 * wsize)).
      rewrite -h1.
      rewrite (addAn w1 (wsize * bn2nat bn1) (wsize * bn2nat bn2)). 
      rewrite (addnC w1 (wsize * bn2nat bn1 + wsize * bn2nat bn2)) // addnA // addnA.
      trivial.
Qed.

Lemma bnadd_correct (z1 z2 : bignum) :
  bn2nat (bnadd z1 z2) = bn2nat z1 + bn2nat z2.
Proof.
rewrite bnadd_correct_Helper //= // addn0.
trivial.
Qed.

(* ===================================================================== *)
(* Multiplication of bignums                                             *)
(* ===================================================================== *)

(* We are now interested in adding bignums: given `z1 z2 : bignum`, we   *)
(* want to compute a bignum `bnadd z1 z2` s.t.                           *)
(*                                                                       *)
(*   bn2nat z = bn2nat z1 * b2nat z2                                     *)
(*                                                                       *)
(* Here, there exists numerous algorithms for computing the multipli-    *)
(* cation of two bignums, with different complexity (from quadratic to   *)
(* quasi-linear). Here, we are again going to use the school-book        *)
(* algorithm to implement the multiplication of bignums. It has a        *)
(* quadratic complexity and is then avoided in real-word bignum          *)
(* libraries:                                                            *)
(*                                                                       *)
(*   proc bnmul(z1 : bignum, z2 : bignum) : bignum {                     *)
(*     z : bignum <- [::]                                                *)
(*     for i = 0 to (size z2) - 1 {                                      *)
(*       z <- bnadd(z, bnshift(bnmul1(z1, z2_i), i))                     *)
(*     }                                                                 *)
(*     return z                                                          *)
(*   }                                                                   *)
(*                                                                       *)
(*   proc bnmul1(z : bignum, w : word) : bignum {                        *)
(*     aout  : bignum <- [::]                                            *)
(*     carry : word   <- 0                                               *)
(*                                                                       *)
(*     for i = 0 to (size z) - 1 {                                       *)
(*       w1, carry <- dword_mul_with_carry(z_i, w, carry)                *)
(*       aout <- aout ++ [:: w1]                                         *)
(*     }                                                                 *)
(*     if (carry != 0) {                                                 *)
(*       aout <- aout ++ [:: carry]                                      *)
(*     }                                                                 *)
(*   }                                                                   *)
(*                                                                       *)
(*  proc dword_mul_with_carry (w1 : word, w2 : word, carry : word) {     *)
(*    w1, w2 <- dword_mul(w1, w2)                                        *)
(*    c , w1 <- word add with_carry(w1, carry, false)                    *)
(*    if (c) {                                                           *)
(*      _, w2 <- word add with carry(w2, 1, false)                       *)
(*    }                                                                  *)
(*    return (w1, w2)                                                    *)
(*  }                                                                    *)
(*                                                                       *)
(*  proc bnshift(w : bignum, n : nat) : bignum {                         *)
(*    for i = 0 to n-1 {                                                 *)
(*      w <- [:: 0] ++ w                                                 *)
(*    }                                                                  *)
(*    return w                                                           *)
(*                                                                       *)
(* where `dword_mul` does the double-word multiplication, whose speci-   *)
(* fication is given below.                                              *)

Context (dword_mul : word -> word -> word * word).

Axiom dword_mul_correct :
  forall (w1 w2 : word),
    let: (w'1, w'2) := dword_mul w1 w2 in
    nat_of_ord w1 * nat_of_ord w2 = w'1 + w'2 * wsize.

(* 6. Implement the functions `bnshift`, `dword_mul_with_carry`,         *)
(*    `bnmul1` & `bnmul`, using the pseudo-code implementations give     *)
(*    above.                                                             *)

Fixpoint bnshift (z : bignum) (n : nat) : bignum :=
  match n with
  | 0 => z
  | S n' => inord (0) :: bnshift z n'
end.

Definition dword_mul_with_carry (w1 w2 c : word) : word * word :=
  (inord 0, inord 0).

Definition bnmul1 (z : bignum) (w : word) : bignum :=
  [::].

Definition bnmul (z1 z2 : bignum) : bignum :=
  [::].

(* 7. Prove the following arithmetical property about `bnshift`.         *)

Lemma bnshiftE (z : bignum) (n : nat) :
  bn2nat (bnshift z n) = bn2nat z * (2^(n * (8 * size))).
Proof. Admitted.

(* 8. Prove that `dword_mul_with_carry` implements a double-word         *)
(*    multiplication with carry, as stated below.                        *)

Lemma dword_mul_with_carry_correct (w1 w2 c : word) :
  let: (w'1, w'2) := dword_mul_with_carry w1 w2 c in
  bn2nat [:: w'1; w'2] = val w1 * val w2 + val c.
Proof. Admitted.

(* 9. Prove that `bnmul1` implements a bignum by word multiplication,    *)
(*    as stated below.                                                   *)

Lemma bnmul1_correct (z : bignum) (w : word) :
  bn2nat (bnmul1 z w) = bn2nat z * val w.
Proof. Admitted.

(* 10. Prove the correctness of `bnmul`, as stated below.                *)

Lemma bnmul_correct (z1 z2 : bignum) :
  bn2nat (bnmul z1 z2) = bn2nat z1 * bn2nat z2.
Proof. Admitted.
